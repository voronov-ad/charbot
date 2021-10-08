package com.hackaton.charbot.feedback;

import lombok.RequiredArgsConstructor;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcOperations;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.stereotype.Repository;

import java.sql.PreparedStatement;
import java.util.List;
import java.util.Optional;

@Repository
@RequiredArgsConstructor
public class JdbcFeedbackStorage implements FeedbackStorage {

    private final NamedParameterJdbcOperations jdbcOperations;

    @Override
    public Integer save(Feedback feedback) {
        try {
            Integer id = jdbcOperations.queryForObject("select id from feedback where url_vacancy = :vacancy and url_candidate= :candidate",
                    new MapSqlParameterSource("vacancy", feedback.getUrl_vacancy())
                            .addValue("candidate", feedback.getUrl_candidate()), Integer.class);
            update(id, feedback);
            return null;
        } catch (EmptyResultDataAccessException e) {
            return saveNew(feedback);
        }

    }

    @Override
    public Optional<Feedback> findById(String id) {
        try {
            return Optional.ofNullable(jdbcOperations.queryForObject("select * from feedback where id = :id",
                    new MapSqlParameterSource("id", Integer.parseInt(id)), new BeanPropertyRowMapper<>(Feedback.class)));
        } catch (EmptyResultDataAccessException e) {
            return Optional.empty();
        }
    }

    private void update(Integer id, Feedback feedback) {
        jdbcOperations.update(" update feedback set label = :label where id = :id",
                new MapSqlParameterSource("id", id)
                        .addValue("label", Boolean.parseBoolean(feedback.getLabel())));
    }

    private Integer saveNew(Feedback feedback) {

        GeneratedKeyHolder keyHolder = new GeneratedKeyHolder();

        String id_column = "id";
        jdbcOperations.getJdbcOperations().update(con -> {
                    PreparedStatement ps = con.prepareStatement("insert into feedback(url_vacancy, url_candidate, label) values(?, ?, ?)",
                            new String[]{id_column});
                    ps.setString(1, feedback.getUrl_vacancy());
                    ps.setString(2, feedback.getUrl_candidate());
                    ps.setBoolean(3, Boolean.parseBoolean(feedback.getLabel()));
                    return ps;
                }
                , keyHolder);
        return (Integer) keyHolder.getKeys().get(id_column);
//        jdbcOperations.update("insert into feedback(url_vacancy, url_candidate, label) values(:vacancy, :candidate, :label)",
//                new MapSqlParameterSource("vacancy", feedback.getUrl_vacancy())
//                        .addValue("candidate", feedback.getUrl_candidate())
//                        .addValue("label", feedback.getLabel()));
    }

    @Override
    public List<Feedback> findAll() {
        return jdbcOperations.getJdbcOperations().query("select * from feedback", new BeanPropertyRowMapper<>(Feedback.class));
    }
}
