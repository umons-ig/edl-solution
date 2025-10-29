import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Tests unitaires pour Surface
 */
public class SurfaceTest {

    @Test
    public void testSurf() {
        assertEquals(6, Surface.surf(2, 3));
        assertEquals(0, Surface.surf(0, 5));
        assertEquals(12, Surface.surf(3, 4));
    }
}
