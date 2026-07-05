package com.example.nowtime;

/**
 * Response body returned by the external POST /epoch endpoint.
 * Deserialized from: {"epoch": 1781517600}
 */
public record EpochResponse(long epoch) {
}
