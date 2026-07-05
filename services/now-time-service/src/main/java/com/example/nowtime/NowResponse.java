package com.example.nowtime;

/**
 * Response returned by this service's GET /now endpoint.
 * Example: {"message": "now is 1781517600"}
 */
public record NowResponse(String message) {
}
