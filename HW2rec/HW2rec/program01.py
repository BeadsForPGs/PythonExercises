# -*- coding: utf-8 -*-
'''
An e-cash system allows the registered users to transfer electronic currency
    units between one another. We shall use the following symbol to denote
    the currency unit: Ħ.
    To transfer Ħ’s, the players resort to intermediary agents who manage the
    transactions at the price of a transaction fee. The transaction fees
    are based on varying percentages decided by the intermediary agents.

The aim of this program is to process a log of transactions between the
    players of the e-cash system and compute:
    1) a list with the final balance of every account of the involved
       player’s accounts;
    2) a list with the final amount earned by every intermediary;
    3) a list in which, for every intermediary, a nested list reports the
       remaining debts of the player’s accounts (0 if no debt was accumulated,
       or a negative integer otherwise).
    Results (1), (2) and (3) should be elements of a tuple.

In particular, the following function should be designed:
    ex1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log)
    where
    – acn1, acn2 and acn3 are the account numbers of player 1, 2 and 3,
      respectively;
    – imd_acn1 and imd_acn2 are the account numbers of intermediaries 1 and 2,
      respectively;
    – init_amount is the initial amount in the accounts of the three players
      (we assume that all players start with the same starting amount);
    – the accounts of intermediaries start with a balance of 0Ħ;
    – transact_log is a list of transactions; every transaction is a tuple,
      which consists of the following elements:
      · a pair of integers indicating the account number of the sender and
        the account number of the receiver;
      · the transferred amount;
      · the account number of the intermediary;
      · the percentage of the transaction fee (to be computed based on the
        transferred amount).

For example, the following tuple:
      ((0x44AE, 0x5B23), 800, 0x1612, 4)
    indicates a transaction transferring 800Ħ from the account number
    0x44AE to the account number 0x5B23, with the help of the intermediary
    who will receive 4% of 800Ħ (thus, 32Ħ) on their account at 0x1612.
    As a result,
    - the balance of the sender (0x44AE) will decrease by
        800 + 32 = 832Ħ,
    - the balance of the recipient (0x5B23) will increase by
        800Ħ,
    - and the intermediary will earn and deposit on their account (0x1612)
        32Ħ.

Notice that if the funds in the sender’s account are insufficient,
    the transaction is declared invalid by the intermediary. The intermediary
    will get the fee anyway from the sender, if there are enough Ħ’s in the
    sender’s account. If the sender’s account cannot pay the transaction fee,
    the intermediary will get all the remaining funds and take its part
    from the next transactions to the sender until the debt is paid.
    In the example above, if there were only 700Ħ in account 0x44AE,
    the intermediary would earn 32Ħ and the amount in 0x44AE would decrease
    to 668Ħ. If there were only 10Ħ in account 0x44AE, the intermediary would
    earn 10Ħ and the amount in 0x44AE would decrease to 0Ħ; also, the
    intermediary would hold a credit of 22Ħ from the sender. The sender would be
    obliged to repay the 22Ħ getting the due amount from the transactions
    received later until the debt is extinguished.

    If a debt is accumulated towards two intermediary agents, funds go to the
    intermediary having the highest credit first, and the remainder goes to
    the other intermediary, for as much as is left. For instance, let player 1
    owe 300Ħ to intermediary 1 and 200Ħ to intermediary 2; as player 1
    receives 400Ħ, 300Ħ are paid to intermediary 1 and 100Ħ are paid to
    intermediary 2. If the same amount is due to both intermediary agents,
    the payback is evenly split. For instance, let player 2 owe 100Ħ to
    intermediary 1 and 100Ħ to intermediary 2; as player 2 receives 100Ħ,
    50Ħ go to each intermediary.

As an example,
    ex1(0x5B23, 0xC78D, 0x44AE, 0x1612, 0x90FF, 1000,
        [ ((0x44AE, 0x5B23),  800, 0x1612,  4),
          ((0x44AE, 0xC78D),  800, 0x90FF, 10),
          ((0xC78D, 0x5B23),  400, 0x1612,  8),
          ((0x44AE, 0xC78D), 1800, 0x90FF, 12),
          ((0x5B23, 0x44AE),  100, 0x1612,  2)
        ]
    returns
    ( [2098, 568, 0], [66, 268], [ [0, 0, 0], [0, 0, -28] ] )
    because all players start with 1000Ħ in their account and, at the end,
    – the balance of player 1 amounts to 2098Ħ,
    – the balance of player 2 amounts to 568Ħ,
    – the balance of player 3 amounts to 0Ħ,
    – intermediary 1 earned 66Ħ,
    – intermediary 2 earned 268Ħ,
    – player 3 still owes 28Ħ to intermediary 2.

NOTE: the timeout for this exercise is of 2 seconds for each test.

WARNING: Make sure that the uploaded file is UTF8-encoded
    (to that end, we recommend you edit the file with Spyder)

'''


def ex1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log):
    # Simplify account and debt initialization
    accounts = {account: init_amount for account in [acn1, acn2, acn3]} | {imd_acn1: 0, imd_acn2: 0}
    debts = {account: {imd_acn1: 0, imd_acn2: 0} for account in [acn1, acn2, acn3]}

    for transaction in transact_log:
        sender, receiver = transaction[0]
        amount, intermediary, fee_percentage = transaction[1:]
        fee = amount * fee_percentage / 100

        # Ensure dynamic handling of any receiver in debts
        if receiver not in debts[sender]:
            debts[sender][receiver] = 0  # Initialize missing receiver with 0 debt

        if accounts[sender] < fee:  # If sender cannot cover fee, allocate what's possible and record debt.
            debts[sender][intermediary] += fee - accounts[sender]
            accounts[intermediary] += accounts[sender]
            accounts[sender] = 0
        else:
            accounts[sender] -= fee
            accounts[intermediary] += fee
            if accounts[sender] >= amount:  # Check if sender can also cover the amount after fee.
                accounts[sender] -= amount
                accounts[receiver] += amount
            else:
                debts[sender][receiver] += amount - accounts[sender]
                accounts[receiver] += accounts[sender]
                accounts[sender] = 0

    # Simplified debt handling with dynamic receiver adjustment
    for account, debt in debts.items():
        for imd_acct, debt_amount in debt.items():
            if accounts[account] >= debt_amount:
                accounts[account] -= debt_amount
                accounts[imd_acct] += debt_amount
                debts[account][imd_acct] = 0

    # Compile final balances and debts
    final_balances = [accounts[acn1], accounts[acn2], accounts[acn3]]
    intermediary_earnings = [accounts[imd_acn1], accounts[imd_acn2]]
    remaining_debts = [[debts[acn1][imd_acn1], debts[acn2][imd_acn1], debts[acn3][imd_acn1]],
                       [debts[acn1][imd_acn2], debts[acn2][imd_acn2], debts[acn3][imd_acn2]]]

    return final_balances, intermediary_earnings, list(map(lambda x: list(map(lambda y: -y, x)), remaining_debts))


if __name__ == '__main__':
    acc1 = 1
    acc2 = 2
    acc3 = 3
    imd1 = 4
    imd2 = 5
    init_amount = 1000
    transact_log = [((acc1, acc2), 1000, imd1, 100), ((acc1, acc3), 100, imd2, 100), ((acc1, acc3), 100, imd1, 100),
                    ((acc2, acc3), 100, imd2, 100), ((acc2, acc1), 200, imd2, 100)]
    print(ex1(acc1, acc2, acc3, imd1, imd2, init_amount, transact_log))
