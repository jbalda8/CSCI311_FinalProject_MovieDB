-- Procedure to add movie

create or replace PROCEDURE add_movie
    (movieTitle IN mm_movie.movie_title%TYPE,
    movieCat IN mm_movie.movie_cat_id%TYPE,
    movieVal IN mm_movie.movie_value%TYPE,
    movieQty IN mm_movie.movie_qty%TYPE,
    output OUT VARCHAR2)
        IS
        max_id NUMBER;
        next_val NUMBER;
    BEGIN
        SELECT MAX(movie_id) INTO max_id FROM mm_movie;
        next_val := max_id + 1;
        INSERT INTO mm_movie (movie_id, movie_title, movie_cat_id, movie_value, movie_qty)
        VALUES (next_val, movieTitle, movieCat, movieVal, movieQty);
        IF SQL%FOUND THEN
            output := 'The movie ' || movieTitle || ' was added!';
        END IF;
        commit;
        EXCEPTION
            WHEN OTHERS THEN
                output := 'There was a constraint error!';
    END;



-- Procedure to add member

create or replace PROCEDURE add_member
    (lastName IN mm_member.last%TYPE,
    firstName IN mm_member.first%TYPE,
    licenseNum IN mm_member.license_no%TYPE,
    licenseState IN mm_member.license_st%TYPE,
    creditCard IN mm_member.credit_card%TYPE,
    mailing IN mm_member.mailing_list%TYPE,
    output OUT VARCHAR2,
    outputID OUT NUMBER)
        IS
        max_id NUMBER;
        next_val NUMBER;
    BEGIN
        SELECT MAX(member_id) INTO max_id FROM mm_member;
        next_val := max_id + 1;
        outputID := next_val;
        INSERT INTO mm_member (member_id, last, first, license_no, license_st, credit_card, mailing_list)
        VALUES (next_val, lastName, firstName, licenseNum, licenseState, creditCard, mailing);
        IF SQL%FOUND THEN
            output := 'Member ' || firstName || ' ' || lastName || ' was added!';
        END IF;
        commit;
        EXCEPTION
            WHEN OTHERS THEN
                output := 'There was a constraint error!';

    END;



-- Function to search and update movie

create or replace FUNCTION update_movie
    (updateID NUMBER,
    updateTitle mm_movie.movie_title%TYPE,
    updateCat mm_movie.movie_cat_id%TYPE,
    updateVal mm_movie.movie_value%TYPE,
    updateQty mm_movie.movie_qty%TYPE)
    RETURN VARCHAR2
        IS
        update_output VARCHAR2(60);
        error_output VARCHAR2(60);
    BEGIN
        UPDATE mm_movie
        SET movie_title = updateTitle, movie_cat_id = updateCat, movie_value = updateVal, movie_qty = updateQty
        WHERE movie_id = updateID;
        IF SQL%FOUND THEN
            update_output := 'The movie was successfully updated!';
        END IF;
        commit;
        RETURN update_output;
        EXCEPTION
            WHEN OTHERS THEN
                error_output := 'There was a constraint error!';
                RETURN error_output;
    END;



-- Function to search and delete movie

  create or replace FUNCTION delete_movie
    (deleteID NUMBER)
    RETURN VARCHAR2
        IS
        delete_output VARCHAR2(60);
        error_output VARCHAR2(60);
    BEGIN
        DELETE FROM mm_movie WHERE movie_id = deleteID;
        IF SQL%FOUND THEN
            delete_output := 'The movie was successfully deleted!';
        END IF;
        commit;
        RETURN delete_output;
        EXCEPTION
            WHEN OTHERS THEN
                error_output := 'There was a constraint error!';
                RETURN error_output;
    END;



-- Function to search and update member

create or replace FUNCTION update_member
    (updateMemberID NUMBER,
    updateColumn VARCHAR2,
    updateValue VARCHAR2)

    RETURN VARCHAR2
        IS
        update_output_mem VARCHAR2(60);
        error_output_mem VARCHAR2(60);
        lv_cursor INTEGER;
        lv_update VARCHAR2(150);
        rows_count NUMBER(1);
    BEGIN
        lv_cursor := DBMS_SQL.OPEN_CURSOR;
        lv_update := 'UPDATE mm_member
                     SET ' || updateColumn || ' = :f_updateValue
                     WHERE member_id = :f_updateMemberID';
        DBMS_SQL.PARSE(lv_cursor, lv_update, DBMS_SQL.NATIVE);
        DBMS_SQL.BIND_VARIABLE(lv_cursor, ':f_updateValue', updateValue);
        DBMS_SQL.BIND_VARIABLE(lv_cursor, ':f_updateMemberID', updateMemberID);
        rows_count := DBMS_SQL.EXECUTE(lv_cursor);
        DBMS_SQL.CLOSE_CURSOR(lv_cursor);
        IF rows_count >= 1 THEN
            update_output_mem := 'The member was successfully updated!';
        END IF;
        commit;
        RETURN update_output_mem;
        EXCEPTION
            WHEN OTHERS THEN
                error_output_mem := 'There was a constraint error!';
                RETURN 'None';
    END;



-- Function to search and delete member

create or replace FUNCTION delete_member
    (deleteMemberID NUMBER)
    RETURN VARCHAR2
        IS
        delete_output_member VARCHAR2(60);
        error_output_member VARCHAR2(60);
    BEGIN
        DELETE FROM mm_member WHERE member_id = deleteMemberID;
        IF SQL%FOUND THEN
            delete_output_member := 'That member was successfully deleted!';
        END IF;
        commit;
        RETURN delete_output_member;
        EXCEPTION
            WHEN OTHERS THEN
                error_output_member := 'There was a constraint error!';
                RETURN error_output_member;
    END;



-- Function to search movie (member) was done inside of python. Since it was
-- just an easy sql command. It was also difficult to print an entire row of
-- data that is inside a function or procedure in oracle. The oracle connection
-- package I used allows to run SQL commands, so it is still extracting that
-- info from my oracle DB



-- Function to rent movie

create or replace FUNCTION rent_movie
    (movieName mm_movie.movie_title%TYPE,
    paymentMethod mm_pay_type.payment_methods%TYPE,
    id_member INTEGER)
    RETURN VARCHAR2
        IS
            maxID NUMBER;
            next_Value NUMBER;
            movie_id_val NUMBER;
            payment_id_val NUMBER;
            current_date DATE;
            rental_output VARCHAR2(60);
            err_rental VARCHAR2(60);
    BEGIN
        current_date := SYSDATE;
        SELECT MAX(rental_id) INTO maxId FROM mm_rental;
        next_Value := maxId + 1;
        SELECT movie_id INTO movie_id_val FROM mm_movie WHERE movie_title = movieName;
        SELECT payment_methods_id INTO payment_id_val FROM mm_pay_type WHERE payment_methods = paymentmethod;
        INSERT INTO mm_rental (rental_id, member_id, movie_id, checkout_date, payment_methods_id)
        VALUES (next_Value, id_member, movie_id_val, current_date, payment_id_val);
        IF SQL%FOUND THEN
            rental_output := movieName || ' was successfully rented!';
        END IF;
        commit;
        RETURN rental_output;
        EXCEPTION
            WHEN OTHERS THEN
                err_rental := 'There was a constraint error!';
                RETURN err_rental;
    END;



  -- Function to return movie

  create or replace FUNCTION return_movie
    (movieName mm_movie.movie_title%TYPE,
    id_member INTEGER)
    RETURN VARCHAR2
        IS
            movie_id_val NUMBER;
            return_output VARCHAR2(60);
            err_return VARCHAR2(60);
    BEGIN
        SELECT movie_id INTO movie_id_val FROM mm_movie WHERE movie_title = movieName;
        UPDATE mm_rental SET CHECKIN_DATE = SYSDATE 
        WHERE movie_id = movie_id_val AND member_id = id_member;
        IF SQL%FOUND THEN
            return_output := movieName || ' was successfully returned!';
        END IF;
        commit;
        RETURN return_output;
        EXCEPTION
            WHEN OTHERS THEN
                err_return := 'There was a constraint error!'; 
                RETURN err_return; 
    END;



-- Trigger when movie is rented

  create or replace TRIGGER take_inventory
    AFTER INSERT ON mm_rental
    FOR EACH ROW

DECLARE
    movie_id_c NUMBER := :NEW.movie_id;
BEGIN
    UPDATE mm_movie SET movie_qty = movie_qty - 1 WHERE movie_id = movie_id_c;
END;



-- Trigger when movie is returned

create or replace TRIGGER add_inventory
    AFTER UPDATE ON mm_rental
    FOR EACH ROW

DECLARE
    movie_id_t NUMBER := :OLD.movie_id;
BEGIN
    UPDATE mm_movie SET movie_qty = movie_qty + 1 WHERE movie_id = movie_id_t;
END;
