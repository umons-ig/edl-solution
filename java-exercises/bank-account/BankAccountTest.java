import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Tests unitaires pour BankAccount
 */
public class BankAccountTest {

    private BankAccount account;

    @Before
    public void setUp() {
        account = new BankAccount("BE12345678", "Jean Dupont", 1000.0);
    }

    @Test
    public void testConstructor() {
        assertEquals("BE12345678", account.getAccountNumber());
        assertEquals("Jean Dupont", account.getOwner());
        assertEquals(1000.0, account.getBalance(), 0.01);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testConstructorWithNullAccountNumber() {
        new BankAccount(null, "Jean Dupont", 1000.0);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testConstructorWithNegativeBalance() {
        new BankAccount("BE12345678", "Jean Dupont", -100.0);
    }

    @Test
    public void testDeposit() {
        account.deposit(500);
        assertEquals(1500.0, account.getBalance(), 0.01);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testDepositWithNegativeAmount() {
        account.deposit(-100);
    }

    @Test
    public void testWithdraw() {
        account.withdraw(300);
        assertEquals(700.0, account.getBalance(), 0.01);
    }

    @Test(expected = IllegalStateException.class)
    public void testWithdrawWithInsufficientBalance() {
        account.withdraw(1500);
    }

    @Test
    public void testTransfer() {
        BankAccount account2 = new BankAccount("BE87654321", "Marie Martin", 500.0);
        account.transfer(account2, 300);
        assertEquals(700.0, account.getBalance(), 0.01);
        assertEquals(800.0, account2.getBalance(), 0.01);
    }
}
