import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Tests unitaires pour Perimetre
 */
public class PerimetreTest {

    @Test
    public void testPerim() {
        assertEquals(10, Perimetre.perim(2, 3, 2));  // (2+3)*2 = 10
        assertEquals(0, Perimetre.perim(0, 0, 5));
        assertEquals(14, Perimetre.perim(3, 4, 2));  // (3+4)*2 = 14
    }
}
