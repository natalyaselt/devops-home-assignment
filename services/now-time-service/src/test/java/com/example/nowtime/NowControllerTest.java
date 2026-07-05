package com.example.nowtime;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.time.Instant;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;

class NowControllerTest {

    @Test
    void wrapsEpochInMessage() {
        EpochClient epochClient = Mockito.mock(EpochClient.class);
        Mockito.when(epochClient.toEpoch(any(Instant.class))).thenReturn(1781517600L);

        NowController controller = new NowController(epochClient);

        NowResponse response = controller.now();

        assertThat(response.message()).isEqualTo("now is 1781517600");
    }
}
