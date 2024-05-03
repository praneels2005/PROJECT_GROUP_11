-- These are all the views that must be created prior to using the UI

CREATE VIEW birthweightrows AS (
    SELECT Trait.animal_id, MAX(alpha_value) AS birth_weight, Trait.when_measured, dob, ROW_NUMBER() OVER (PARTITION BY Trait.animal_id ORDER BY Trait.when_measured DESC) AS row_num 
    FROM Goat JOIN Trait ON Goat.animal_id = Trait.animal_id
    WHERE trait_code = 357 AND alpha_value <> ''
    GROUP BY Trait.animal_id, Trait.when_measured, dob
    HAVING when_measured = MAX(when_measured)
);

CREATE VIEW birthweights AS (
    SELECT animal_id, birth_weight, when_measured, dob
    FROM birthweightrows WHERE row_num=1
);

CREATE VIEW wt1 AS (SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3)
FROM birthweights
WHERE EXTRACT(YEAR FROM dob) = 2013);

CREATE VIEW wt2 AS (SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3)
FROM birthweights
WHERE EXTRACT(YEAR FROM dob) = 2014);

CREATE VIEW wt3 AS (SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3)
FROM birthweights
WHERE EXTRACT(YEAR FROM dob) = 2015);

CREATE VIEW wt4 AS (SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3)
FROM birthweights
WHERE EXTRACT(YEAR FROM dob) = 2016);

CREATE VIEW wt5 AS (SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3)
FROM birthweights
WHERE EXTRACT(YEAR FROM dob) = 2017);

CREATE VIEW wt6 AS (SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3)
FROM birthweights
WHERE EXTRACT(YEAR FROM dob) = 2018);

CREATE VIEW wt7 AS (SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3)
FROM birthweights
WHERE EXTRACT(YEAR FROM dob) = 2019);

CREATE VIEW wt8 AS (SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3)
FROM birthweights
WHERE EXTRACT(YEAR FROM dob) = 2020);

CREATE VIEW wt9 AS (SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3)
FROM birthweights
WHERE EXTRACT(YEAR FROM dob) = 2021);

CREATE VIEW wt10 AS (SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3)
FROM birthweights
WHERE EXTRACT(YEAR FROM dob) = 2022);

CREATE VIEW wt11 AS (SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3)
FROM birthweights
WHERE EXTRACT(YEAR FROM dob) = 2023);

CREATE VIEW minmax AS (SELECT MAX(birth_weight) AS max, MIN(birth_weight) AS min FROM birthweights);

CREATE VIEW doebirthing AS (
    SELECT t1.animal_id AS mom, t1.tag, t1.dob AS momDOB, t2.dob AS kidDOB, t2.animal_id AS kid, t2.dam, EXTRACT(YEAR FROM t2.dob) - EXTRACT(YEAR FROM t1.dob) - CASE
    WHEN
    (EXTRACT(MONTH FROM t1.dob) > EXTRACT(MONTH FROM t2.dob))
    OR
    ((EXTRACT(MONTH FROM t1.dob) = EXTRACT(MONTH FROM t2.dob)) AND (EXTRACT(DAY FROM t1.dob) > EXTRACT(DAY FROM t2.dob)))
    THEN 1 ELSE 0
    END AS momAGE
    FROM Goat t1 JOIN Goat t2 ON t1.tag = t2.dam
);

CREATE VIEW single AS (
    SELECT Trait.animal_id AS damID, alpha_value, Trait.when_measured, t1.tag, t2.animal_id AS kidID, t2.dam, t2.dob
    FROM Trait
    JOIN Goat t1 ON Trait.animal_id = t1.animal_id
    JOIN Goat t2 ON t1.tag = t2.dam
    WHERE trait_code = 486 AND alpha_value = ''
);

CREATE VIEW twin AS (
    SELECT Trait.animal_id AS damID, alpha_value, Trait.when_measured, t1.tag, t2.animal_id AS kidID, t2.dam, t2.dob
    FROM Trait
    JOIN Goat t1 ON Trait.animal_id = t1.animal_id
    JOIN Goat t2 ON t1.tag = t2.dam
    WHERE trait_code = 486 AND alpha_value = '2 Twins'
);

CREATE VIEW triplet AS (
    SELECT Trait.animal_id AS damID, alpha_value, Trait.when_measured, t1.tag, t2.animal_id AS kidID, t2.dam, t2.dob
    FROM Trait
    JOIN Goat t1 ON Trait.animal_id = t1.animal_id
    JOIN Goat t2 ON t1.tag = t2.dam
    WHERE trait_code = 486 AND alpha_value = '3 Triplets'
);

CREATE VIEW singleID AS (SELECT kidID, dob FROM single GROUP BY kidID, dob HAVING COUNT(*) = 1);

CREATE VIEW twinID AS (SELECT kidID, dob FROM twin GROUP BY kidID, dob HAVING COUNT(*) = 2);

CREATE VIEW tripletID AS (SELECT kidID, dob FROM triplet GROUP BY kidID, dob HAVING COUNT(*) = 3);

CREATE VIEW singleweights AS (SELECT animal_id AS singleID, alpha_value AS birth_weight FROM singleID JOIN Trait ON kidID = animal_id WHERE trait_code = 357 AND alpha_value <> '');

CREATE VIEW twinweights AS (SELECT animal_id AS singleID, alpha_value AS birth_weight FROM twinID JOIN Trait ON kidID = animal_id WHERE trait_code = 357 AND alpha_value <> '');

CREATE VIEW tripletweights AS (SELECT animal_id AS singleID, alpha_value AS birth_weight FROM tripletID JOIN Trait ON kidID = animal_id WHERE trait_code = 357 AND alpha_value <> '');

CREATE VIEW firstmomkids AS (
    SELECT Vaccine.animal_id AS momID, activity_code, when_measured, t1.tag, t2.animal_id as kidID, t2.dam, t2.dob
    FROM Vaccine
    JOIN Goat t1 ON Vaccine.animal_id = t1.animal_id
    JOIN Goat t2 ON t1.tag = t2.dam
    WHERE activity_code = 892
);

CREATE VIEW oldermomkids AS (
    SELECT Vaccine.animal_id AS momID, activity_code, when_measured, t1.tag, t2.animal_id as kidID, t2.dam, t2.dob
    FROM Vaccine
    JOIN Goat t1 ON Vaccine.animal_id = t1.animal_id
    JOIN Goat t2 ON t1.tag = t2.dam
    WHERE activity_code = 895 OR activity_code = 898
);

CREATE VIEW firstmomweights AS (
    SELECT kidID, alpha_value AS birth_weight
    FROM firstmomkids JOIN Trait ON kidID = animal_id
    WHERE trait_code = 357 AND alpha_value <> ''
);

CREATE VIEW oldermomweights AS (
    SELECT kidID, alpha_value AS birth_weight
    FROM oldermomkids JOIN Trait ON kidID = animal_id
    WHERE trait_code = 357 AND alpha_value <> ''
);

CREATE VIEW firstmomkidnum AS (
    SELECT Vaccine.animal_id AS momID, activity_code, Vaccine.when_measured, Trait.animal_id, alpha_value
    FROM Vaccine
    JOIN Trait ON Vaccine.animal_id = Trait.animal_id 
    WHERE activity_code = 892 AND trait_code = 486 AND alpha_value <> ''
);

CREATE VIEW oldermomkidnum AS (
    SELECT Vaccine.animal_id AS momID, activity_code, Vaccine.when_measured, Trait.animal_id, alpha_value
    FROM Vaccine
    JOIN Trait ON Vaccine.animal_id = Trait.animal_id 
    WHERE (activity_code = 895 OR activity_code = 898) AND trait_code = 486 AND alpha_value <> ''
);

CREATE VIEW vaccinelist AS (
    SELECT Vaccine.animal_id AS mom, activity_code AS vaccine, Trait.animal_id AS kid, alpha_value AS birth_weight
    FROM Vaccine
    JOIN Goat t1 ON Vaccine.animal_id = t1.animal_id
    JOIN Goat t2 ON t1.tag = t2.dam
    JOIN Trait ON t2.animal_id = Trait.animal_id
    WHERE Trait.trait_code = 357 AND alpha_value <> ''
);
