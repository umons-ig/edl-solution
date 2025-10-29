import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Tests unitaires pour Money
 */
public class MoneyTest {

    @Test
    public void testAmount() {
        Money instance = new Money(12, "EUR");
        assertEquals(12, instance.amount());
    }

    /**
     * TODO: EXERCICE 2 - Écrire le test testCurrency()
     *
     * S'inspirer de testAmount() ci-dessus
     * Utiliser assertEquals() au lieu de assertNotEquals()
     */
    @Test
    public void testCurrency() {
        // TODO: Créer une Money avec currency "EUR"
        // TODO: Vérifier que currency() retourne "EUR"
        Money instance = new Money(12, "EUR");
        String expected = "EUR";
        String result = instance.currency();
        assertEquals(expected, result);
    }

    @Test
    public void testAdd_Money() throws Exception {
        Money instance = new Money(12, "EUR");
        Money expected = new Money(24, "EUR");
        Money result = instance.add(new Money(12, "EUR"));

        assertEquals(expected.amount(), result.amount());
        assertEquals(expected.currency(), result.currency());
    }

    /**
     * TODO: EXERCICE 3 - Écrire le test testAdd()
     *
     * S'inspirer de testAdd_Money() ci-dessus
     */
    @Test
    public void testAdd() throws Exception {
        // TODO: Créer une Money de 10 EUR
        // TODO: Ajouter 5 EUR
        // TODO: Vérifier que le résultat est 15 EUR
        Money instance = new Money(10, "EUR");
        Money toAdd = new Money(5, "EUR");
        Money result = instance.add(toAdd);

        assertEquals(15, result.amount());
        assertEquals("EUR", result.currency());
    }
}
