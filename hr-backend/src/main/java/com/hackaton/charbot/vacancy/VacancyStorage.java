package com.hackaton.charbot.vacancy;

import java.util.List;
import java.util.Optional;

public interface VacancyStorage {

    void save(Vacancy vacancy);

    Optional<Vacancy> findById(String id);

    List<String> findAllIds();
}
