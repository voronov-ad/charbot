package com.hackaton.charbot.feedback;

import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import javax.websocket.server.PathParam;
import java.util.List;

@RestController
@RequestMapping(path = "/api/v1/feedback")
@RequiredArgsConstructor
public class FeedbackController {

    private final FeedbackStorage storage;

    @PostMapping
    ResponseEntity<?> register(@RequestBody Feedback feedback) {
        Integer id = storage.save(feedback);
        return ResponseEntity.ok(id);
    }

    @GetMapping(path = "/{id}")
    Feedback byId(@PathVariable String id) {
        return storage.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NO_CONTENT, "Not found feedback by id " + id));
    }

    @GetMapping
    List<Feedback> findAll() {
        return storage.findAll();
    }
}
