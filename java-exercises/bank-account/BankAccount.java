/**
 * Classe BankAccount - Gestion de compte bancaire
 * Exercice : Implémenter les méthodes avec validation
 */
public class BankAccount {

    private String accountNumber;
    private String owner;
    private double balance;

    public BankAccount(String accountNumber, String owner, double initialBalance) {
        if (accountNumber == null || accountNumber.trim().isEmpty()) {
            throw new IllegalArgumentException("Account number cannot be null or empty");
        }
        if (owner == null || owner.trim().isEmpty()) {
            throw new IllegalArgumentException("Owner cannot be null or empty");
        }
        if (initialBalance < 0) {
            throw new IllegalArgumentException("Initial balance cannot be negative");
        }

        this.accountNumber = accountNumber;
        this.owner = owner;
        this.balance = initialBalance;
    }

    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
        this.balance += amount;
    }

    public void withdraw(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
        if (this.balance < amount) {
            throw new IllegalStateException("Insufficient balance");
        }
        this.balance -= amount;
    }

    public void transfer(BankAccount destination, double amount) {
        if (destination == null) {
            throw new IllegalArgumentException("Destination account cannot be null");
        }
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
        this.withdraw(amount);
        destination.deposit(amount);
    }

    public double getBalance() {
        return balance;
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public String getOwner() {
        return owner;
    }
}
