-- SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUser that computes
-- and store the average weighted score for a student.
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
        DECLARE weighted_score_average FLOAT;
        DECLARE weightXscore INT;
        DECLARE weight_sum INT;


        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO weightXscore, weight_sum
        FROM  corrections c
        INNER JOIN projects p
        ON c.project_id = p.id
        WHERE c.user_id = user_id;

        SET weighted_score_average = IFNULL(weightXscore / NULLIF(weight_sum, 0), 0);

        UPDATE users
        SET average_score = weighted_score_average
        WHERE id = user_id;

END //
DELIMITER ;


-- SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUsers that computes
-- and store the average weighted score for all student.
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE done INT DEFAULT 0;
	DECLARE user_id INT;
	DECLARE cur CURSOR FOR SELECT id FROM users;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

	OPEN cur;

	read_loop: LOOP
	FETCH cur INTO user_id;
	IF done THEN
		LEAVE read_loop;
	END IF;

	CALL ComputeAverageWeightedScoreForUser(user_id);

	END LOOP;

	CLOSE cur;
END //
DELIMITER ;
