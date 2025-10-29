/**
 * Classe Money - Gestion de monnaie et devise
 * SOLUTION COMPLÈTE
 */
public class Money {

    private int mAmount;
    private String mCurrency;

    public Money(int amount, String currency) {
        this.mAmount = amount;
        this.mCurrency = currency;
    }

    public int amount() {
        return mAmount;
    }

    public String currency() {
        return mCurrency;
    }

    /**
     * Addition de deux monnaies
     * Les devises doivent être identiques
     */
    public Money add(Money m) throws Exception {
        if (this.currency().equals(m.currency())) {
            return new Money(this.amount() + m.amount(), this.currency());
        }
        throw new Exception("Not Same currency");
    }
}
