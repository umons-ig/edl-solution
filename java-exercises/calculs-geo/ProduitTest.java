import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Tests unitaires pour Produit
 */
public class ProduitTest {

    @Test
    public void testMult() {
        assertEquals(6, Produit.mult(2, 3));
        assertEquals(0, Produit.mult(0, 5));
        assertEquals(-6, Produit.mult(-2, 3));
    }
}
