package com.hackaton.charbot.resume;

import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import javax.websocket.server.PathParam;

@RestController
@RequestMapping(path = "/api/v1/resume")
@RequiredArgsConstructor
public class ResumeController {

    private final ResumeStorage storage;

    @GetMapping(path = "/{id}")
    Resume getById(@PathVariable String id) {
        return storage.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NO_CONTENT, "Resume not found by id" + id));
    }
}
