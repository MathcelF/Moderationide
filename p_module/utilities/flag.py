class Flag:
    class Get:
        m_flag = {'supporter': [0, 0x1], 'moderator': [1, 0x2], 'administrator': [2, 0x4], 'developer': [3, 0x8]}
        s_flag = {'user': [0, 0x1], 'customer': [1, 0x2], 'donator': [2, 0x4], 'boronidian': [3, 0x8]}
        m_list = ['supporter', 'moderator', 'administrator', 'developer']
        s_list = ['user', 'customer', 'donator', 'imperator']

        @staticmethod
        def validate_type(to_check):
            """
            Checks if the argument is a hex; Format is 0xHexadecimal; integer or string.
            Example of how argument can look like (same Value; different Types):
                -> Value: Developer; Types: 0x8 [Hex] | 8 [Integer] | 'Developer' [String]
                -> Values: Admin, Developer; Types: 0xC [Hex] | 12 [Integer] 'Developer', 'Admin' [List of Strings]

            Returns 'status' x00, 'returnValue' type [or error message]:
            -> If to_check is a valid type return will be: 200 (success) type: the type
             -> If to_check is hex, but it is something like 0xJ (0-9, A-F) it will return:
             200, Contains invalid Hexadecimal characters!.
            In other modules you will bump into 'status' 100 a lot.
            I use it as a return None but with proper error_handling to inform the user about his mistake for example.
            """
            if to_check[:2] == '0x':
                if all(x in '0123456789abcdefABCDEF' for x in to_check[2:]):
                    return {'status': 200, 'returnValue': 'hex'}
                return {'status': 100, 'returnValue': '{} Contains invalid Hexadecimal characters!'.format(to_check)}

            if isinstance(to_check, int):
                return {'status': 200, 'returnValue': 'hex'}
            return {'status': 200, 'returnValue': 'string'}

        @staticmethod
        def convert_to_binary(num, bool_conversion=False):
            """
            Returns a binary from a hex/integer [flag]
            ``bool_conversion`` is optional. If it is true:
                it will return e.g. True, False, False, True
                instead of 1, 0, 0, 1.
            """
            if bool_conversion:
                return [bool(num & (1 << n)) for n in range(len(bin(num)) - 2)]
            return [int(bool(num & (1 << n))) for n in range(len(bin(num)) - 2)]

        @staticmethod
        def flag_permissions(num, keyword):
            """
            Converts a hex/integer into a binary and receives the appropriate Key of flag's list
                0xD/13 -> 1 1 0 0 -> Admin, Developer ....
                ! 1 1 0 0 is read backwards -> 0 0 1 1 (Supporter / Moderator / Admin/ Developer)

            Returns (also shown above) the jey/s of flag's list from converted argument: num (hex/integer)
            """
            to_return = []
            for c, i in enumerate(Flag.Get.convert_to_binary(num)):
                if i and keyword == 'm_flag':
                    to_return.append(Flag.Get.m_list[c])
                elif i and keyword == 's_flag':
                    to_return.append(Flag.Get.s_list[c])
            return to_return

        @staticmethod
        def get_hex(arg, flag_type):
            """
            Converts List or String related to the flag_type to the hexadecimal system.
                e.g 'Moderator' in m_flag is 0x2. so arg: 'Moderator', flag_type: 'm_flag'
                will return 0x2 because 'Moderator' is in m_flag.

            Returns status_code 200 if successful. returnMessage which will be implemented as the response:
            and returnValue: the flag hex of the argument.
            """
            if isinstance(arg, list):
                flagCounter = 0
                for i in arg:
                    if flag_type == 'm_flag':
                        if i in Flag.Get.m_list:
                            flagCounter += (Flag.Get.m_flag[i][1])
                    elif flag_type == 's_flag':
                        if i in Flag.Get.s_list:
                            flagCounter += (Flag.Get.s_flag[i][1])
                if flagCounter == 0:
                    return {'status': 100, 'returnValue': 'Arguments are not valid flag_names'}
                return {'status': 200, 'returnValue': flagCounter}
            if isinstance(arg, str):
                if flag_type == 'm_flag' and arg in Flag.Get.m_list:
                    return {'status': 200, 'returnValue': Flag.Get.m_flag[arg][1]}
                elif flag_type == 's_flag' and arg in Flag.Get.s_list:
                    return {'status': 200, 'returnValue': Flag.Get.s_flag[arg][1]}
                return {'status': 100, 'returnValue': 'Error from Syntax or Argument'}

        @staticmethod
        def add_flag_calculation(user_flag, add_flag, key):
            """
            Function checks if user has duplicates flag to avoid errors:
              -> User's Flag is (0xD | 1101); We want to add (0x6 | 0110)
               -> We can't go over (0xF | 1111): Error is at (0x4 | 0100)
                -> We are subtracting 0x4 from 0x6, and so we get (0x2 | 0010)

            Function finds duplicates and subtracts them from add_flag.
            ``flag_comparison`` compares user_flag and add_flag (converted)
                -> to find duplicates which will be removed on the next step.

            ``prefix`` is obvious: I have 1 cookies is wrong:
                -> If the amount is singular, the text will be I have 1 cookie.
                 -> As we have strings, and we format them with the prefix:
                 = We will get better and clean text without Flag/s.

            Returns status_code 20X if successful. returnMessage which will be implemented as the response:
            and returnValue: the flag, as this function's purpose is to calculate and compensate,
            """
            users_flags = Flag.Get.flag_permissions(user_flag, key)
            flags_to_add = Flag.Get.flag_permissions(add_flag, key)
            flag_comparison = list(set(flags_to_add).intersection(set(users_flags)))
            print(users_flags, flags_to_add, flag_comparison)
            prefix = '' if len(flag_comparison) == 1 else 's'
            if len(flag_comparison) == len(flags_to_add):
                return {'status': 100, 'returnMessage': 'Can\'t add Flags: User already has these Flags!'}
            if len(flag_comparison) != 0:
                add_flag -= Flag.Get.get_hex(flag_comparison, key)['returnValue']
                non_duplicates = [x for x in flags_to_add if x not in flag_comparison]
                already_has = 'User already has Flag{}: **`{}`**'.format(prefix, '` `'.join(flag_comparison))
                removing_duplicates = '||Removing: **`{}`** Flag{} **[Duplicates]**||'.format('` `'.join(flag_comparison), prefix)
                adding_non_duplicates = 'Adding **[Non-Duplicate]** Flag{}: **`{}`**'.format(prefix, '` `'.join(non_duplicates))
                return {'status': 201, 'returnValue': add_flag, 'returnMessage': [already_has, removing_duplicates, adding_non_duplicates]}

            adding_text = 'Adding Flag{}:  **`{}`**'.format(prefix, '` `'.join(flags_to_add))
            return {'status': 200, 'returnValue': add_flag, 'returnMessage': [adding_text]}

        @staticmethod
        def sub_flag_calculation(user_flag, sub_flag, key):
            """
            Function checks if user has duplicates flag to avoid errors:
              -> User's Flag is (0x3 | 0011); We want to sub (0x2 | 0010)
               -> We can't subtract (0x6 | 0110) e.g, so:
                -> We are subtracting 0x4 from 0x6, and so we get (0x2 | 0010)
                This example shows if we sub 0x6 instead of 0x2;
                But I need to have this clear.

            Function finds non-existing flags and subtracts them from add_flag.
            ``flag_comparison`` compares user_flag and add_flag (converted)
                -> to find existing flags: so we can re-calculate the real flag

            ``prefix`` is obvious: I have 1 cookies is wrong:
                -> If the amount is singular, the text will be I have 1 cookie.
                 -> As we have strings, and we format them with the prefix:
                 = We will get better and clean text without Flag/s.

            Returns status_code 20X if successful. returnMessage which will be implemented as the response:
            and returnValue: the flag, as this function's purpose is to calculate and compensate,
            """
            users_flags = Flag.Get.flag_permissions(user_flag, key)
            flags_to_sub = Flag.Get.flag_permissions(sub_flag, key)
            flag_comparison = list(set(flags_to_sub).intersection(set(users_flags)))
            prefix = '' if len(flag_comparison) == 1 else 's'
            if len(flag_comparison) != 0:
                user_flag -= Flag.Get.get_hex(flag_comparison, key)['returnValue']
                invalid_flag = [x for x in flags_to_sub if x not in flag_comparison]
                if len(invalid_flag) > 0:
                    missing = 'User does not have Flag{}: **`{}`**'.format(prefix, '` `'.join(invalid_flag))
                    removing_missing = '||Removing: **`{}`** Flag{} **[Missing]**||'.format('` `'.join(invalid_flag), prefix)
                    adding_existing = 'Deducting **[Existent]** Flag{}: **`{}`**'.format(prefix, '` `'.join(flag_comparison))
                    return {'status': 201, 'returnValue': user_flag, 'returnMessage': [missing, removing_missing, adding_existing]}
                deducting_text = 'Deducting Flag{}:  **`{}`**'.format(prefix, '` `'.join(flags_to_sub))
                return {'status': 200, 'returnValue': user_flag, 'returnMessage': [deducting_text]}
            return {'status': 100, 'returnMessage': 'Can\'t deduct Flags: User does not have these Flags!'}
