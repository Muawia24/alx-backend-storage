-- SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUser that computes
-- and store the average weighted score for a student.
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	DECLARE weighted_score_average DECIMAL(10, 2);
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
