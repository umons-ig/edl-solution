import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Tests unitaires pour Addition
 */
public class AdditionTest {

    @Test
    public void testAdd() {
        assertEquals(5, Addition.add(2, 3));
        assertEquals(0, Addition.add(0, 0));
        assertEquals(1, Addition.add(-1, 2));
    }
}
