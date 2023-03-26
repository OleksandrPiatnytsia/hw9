def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ValueError as et:

            print(et)

        except IndexError as et:

            print(et)

    return wrapper


@input_error
def get_func_from_text(input_text: str):
    input_command = input_text.strip().split(" ")[0]

    if not input_command:
        raise IndexError("No command inputted! Try again")

    for command, func in COMMANDS_LIST.items():
        if input_command == command:
            return func, input_text.replace(command, "").strip()

    return no_command, input_command


def help(*args):
    return f"""Hello! I am contact manager bot!
I can add new contact with command: 'add', use following syntax: add 'contact name, phone'
I can change existing contact with command: 'change', use following syntax: change 'contact name, phone'
I can find contact by phone with command: 'phone', use following syntax: phone 'contact name'
For viewing all list use command: 'show'
For exit use commands: 'stop', 'close', 'exit' or 'good bye'"""


@input_error
def hello(*args):
    return f"How can I help you?"


@input_error
def no_command(*args):
    return f"No such '{args[0]}' command use command 'help'"

    # raise ValueError("No such command use command")


@input_error
def add(*args):
    input_params = args[0]
    params_list = input_params.split(",")
    if len(params_list) == 1:
        raise ValueError(f"Inputted not correctly data: {input_params}: ',' - is missing: ''")
    elif len(params_list) > 2:
        raise ValueError(f"Inputted not correctly data: {input_params}: to mach parameters!")

    phone = params_list[1].strip()

    for ch in phone:
        if not ch.isdigit():
            raise ValueError(f"Inputted not correctly data: {params_list[1]}: must consist only digits!")

    contact_name = params_list[0].strip().title()

    if CONTACT_DICT.get(contact_name):
        raise IndexError(f"Inputted name: '{contact_name}' already exist")

    for k, v in CONTACT_DICT.items():
        if v == phone:
            raise IndexError(
                f"Inputted phone: '{phone}' already have contact: '{get_formated_contact(contact_name, phone)}'")

    CONTACT_DICT.update({contact_name: phone})

    return f"{get_formated_contact(contact_name, phone)} - added to contacts"


@input_error
def change(*args):
    input_params = args[0]
    params_list = input_params.split(",")
    if len(params_list) == 1:
        raise ValueError(f"Inputted not correctly data: {input_params}: ',' - is missing: ''")
    elif len(params_list) > 2:
        raise ValueError(f"Inputted not correctly data: {input_params}: to mach parameters!")

    phone = params_list[1].strip()

    for ch in phone:
        if not ch.isdigit():
            raise ValueError(f"Inputted not correctly data: {params_list[1]}: must consist only digits!")

    contact_name = params_list[0].strip().title()

    for k, v in CONTACT_DICT.items():
        if v == phone:
            raise IndexError(
                f"Inputted phone: '{phone}' already have contact: '{get_formated_contact(contact_name, phone)}'")

    contact_exist = CONTACT_DICT.get(contact_name)

    CONTACT_DICT.update({contact_name: phone})

    if contact_exist:
        return f"{get_formated_contact(contact_name, phone)} - is changed"
    else:
        return f"{get_formated_contact(contact_name, phone)} - added to contacts"


@input_error
def phone(*args):
    input_contact_name = args[0]

    result_list = []
    if input_contact_name:
        for contact_name, phone in CONTACT_DICT.items():
            if input_contact_name.lower() in contact_name.lower():
                result_list.append(get_formated_contact(contact_name, phone))
    else:
        raise ValueError("Parameter 'contact name' is empty, try again or use 'help'")

    if result_list:
        return "\n".join(result_list)
    else:
        return f"There are no '{input_contact_name}' matches among contacts"


@input_error
def show_all(*args):
    result_list = []
    for contact_name, phone in CONTACT_DICT.items():
        result_list.append(get_formated_contact(contact_name, phone))

    return "\n".join(result_list)


@input_error
def exit(*args):
    return f"Work ended"


def get_formated_contact(contact_name, phone):
    return f"{contact_name}: {phone}"


COMMANDS_LIST = {"hello": hello,
                 "help": help,
                 "add": add,
                 "change": change,
                 "phone": phone,
                 "show all": show_all,
                 "show": show_all,
                 "good bye": exit,
                 "close": exit,
                 "stop": exit,
                 "exit": exit}

CONTACT_DICT = {"Bob Marley": "0967845456",
                "Borys Jonson": "0967845456",
                "Lara Croft": "0967845456",
                "Bred Pitt": "0967845456"}



def main():
    while True:

        input_data = input("Input command (For help use command 'help'):")

        result = get_func_from_text(input_data)

        if result:
            command, data = result

            result_comand = command(data)

            if result_comand:
                print(result_comand)

            if command == exit:
                break


if __name__ == '__main__':
    main()
