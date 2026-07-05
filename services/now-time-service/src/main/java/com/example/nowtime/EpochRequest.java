package com.example.nowtime;

/**
 * Request body sent to the external POST /epoch endpoint.
 * Serialized as: {"date": "2026-06-15T10:00:00Z"}
 */
public record EpochRequest(String date) {
}
