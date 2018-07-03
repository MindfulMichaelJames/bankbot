def process_request(response_string, account):
    response_list = response_string.split()
    command = response_list[0]
    if len(response_list) > 1:
        response_args = response_list[1:]
    else:
        response_args = None
    if command == "get_balance":
        return get_balance(account)
    elif command == "get_beneficiaries":
        return get_beneficiaries(account)
    elif command == "pay_recipient":
        return pay_recipient(account, response_args)
    elif command == "get_transactions":
        return get_transactions(account)
    elif command == "get_debit_orders":
        return get_debit_orders(account)
    elif command == "return_default":
        return return_default()


def get_balance(account):
    return "You have R{} in your account".format(account['balance'])


def get_beneficiaries(account):
    return "These are the people in your list of beneficiaries:\n{}".format('\n'.join(account['beneficiaries']))


def pay_recipient(account, payment_args):
    if account['balance'] < eval(payment_args[1]):
        return "You do not have enough money in your account to complete this transaction"
    else:
        return "R{} paid to {}.".format(payment_args[0], payment_args[1])


def get_transactions(account):
    return "Here are your latest payments: {}".format("\n".join(account['transactions']))


def get_debit_orders(account):
    return "Here are your debit orders: {}".format("\n".join(account['orders']))


def return_default():
    return "I don't understand. What do you mean?"
