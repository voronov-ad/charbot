package com.hackaton.charbot.vacancy;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcOperations;
import org.springframework.jdbc.core.support.SqlLobValue;
import org.springframework.jdbc.support.lob.DefaultLobHandler;
import org.springframework.jdbc.support.lob.LobHandler;
import org.springframework.stereotype.Repository;

import java.sql.Types;
import java.util.List;
import java.util.Optional;

@Repository
@RequiredArgsConstructor
public class JdbcVacancyStorage implements VacancyStorage {
    private final NamedParameterJdbcOperations jdbcTempalte;
    ObjectMapper objectMapper = new ObjectMapper();

    @SneakyThrows
    @Override
    public void save(Vacancy vacancy) {
        MapSqlParameterSource in = new MapSqlParameterSource("id", vacancy.getId())
        .addValue("vacancy_data", new SqlLobValue(objectMapper.writeValueAsString(vacancy),
                new DefaultLobHandler()), Types.CLOB)
                .addValue("vacancy_link", vacancy.getLink());
        jdbcTempalte.update("insert into vacancy(id, vacancy_data, vacancy_link) values (:id, :vacancy_data, :vacancy_link) on conflict(id) " +
                "do update set vacancy_data = excluded.vacancy_data, vacancy_link= excluded.vacancy_link", in);
    }

    @SneakyThrows
    @Override
    public Optional<Vacancy> findById(String id) {
        LobHandler lobHandler = new DefaultLobHandler();

        try {
            String value = jdbcTempalte.queryForObject("select vacancy_data from vacancy where id = :id",
                    new MapSqlParameterSource("id", id), (rs, rowNum) -> lobHandler.getClobAsString(rs, 1));
            return Optional.ofNullable(objectMapper.readValue(value, Vacancy.class));
        } catch (EmptyResultDataAccessException e) {
            return Optional.empty();
        }
    }

    @Override
    public List<String> findAllIds() {
        return jdbcTempalte.getJdbcOperations().queryForList("select id from vacancy", String.class);
    }
}
