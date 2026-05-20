class Bank:
    bank_name = 'SBI'
    bank_ifsc = 12345
    bank_roi = 6
    bank_address = 'KGF'
sam = Bank()
cuku = Bank()

print(Bank.bank_ifsc)
print(sam.bank_name)
Bank.bank_roi = 7
print(Bank.bank_roi)
cuku.bank_roi=5
print(Bank.bank_roi)
print(cuku.bank_roi)