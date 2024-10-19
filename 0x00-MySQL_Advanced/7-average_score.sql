-- a SQL script that creates a stored procedure
-- ComputeAverageScoreForUser that computes and store
-- the average score for a student
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
	DECLARE score_average INT;

	SELECT SUM(score) / COUNT(score)
	INTO score_average
	FROM corrections
	WHERE corrections.user_id = user_id;

	UPDATE users
	SET average_score = score_average
	WHERE id = user_id;

END //
DELIMITER ;
