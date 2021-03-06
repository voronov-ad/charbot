package com.hackaton.charbot.resume;

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
public class JsbcResumeStorage implements ResumeStorage {
    private final NamedParameterJdbcOperations jdbcTempalte;
    ObjectMapper objectMapper = new ObjectMapper();

    @SneakyThrows
    @Override
    public void save(Resume resume) {
        MapSqlParameterSource in = new MapSqlParameterSource("id", resume.getId())
        .addValue("resume_data", new SqlLobValue(objectMapper.writeValueAsString(resume),
                new DefaultLobHandler()), Types.CLOB)
        .addValue("resume_link", resume.getLink());
        jdbcTempalte.update("insert into resume(id, resume_data, resume_link) values (:id, :resume_data, :resume_link) " +
                "on conflict(id) do update set resume_data = excluded.resume_data, resume_link = excluded.resume_link", in);
    }

    @SneakyThrows
    @Override
    public Optional<Resume> findById(String id) {
        LobHandler lobHandler = new DefaultLobHandler();

        String value = null;
        try {
            value = jdbcTempalte.queryForObject("select resume_data from resume where id = :id",
                    new MapSqlParameterSource("id", id), (rs, rowNum) -> lobHandler.getClobAsString(rs, 1));
            return Optional.ofNullable(objectMapper.readValue(value, Resume.class));
        } catch (EmptyResultDataAccessException e) {
            return Optional.empty();
        }
    }

    @Override
    public List<String> findAllIds() {
        return jdbcTempalte.getJdbcOperations().queryForList("select id from resume", String.class);
    }
}
