package com.hackaton.charbot.vacancy;

import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

@RestController
@RequestMapping(path = "/api/v1/vacancy")
@RequiredArgsConstructor
public class VacancyController {

    private final VacancyStorage storage;

    @PostMapping(consumes = "application/json")
    void register(@RequestBody Vacancy vacancy){
        storage.save(vacancy);
    }

    @GetMapping(path = "/{id}")
    Vacancy getById(@PathVariable String id) {
        return storage.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NO_CONTENT, "Vacancy not found by id" + id));
    }

    @GetMapping()
    List<String> get_ids() {
        return storage.findAllIds();
    }
}
