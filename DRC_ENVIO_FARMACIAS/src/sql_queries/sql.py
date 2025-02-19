# SQL to collect all CPFs of dependents
SQL_DEPENDENTS_CPFS = """ 
    SELECT
        DISTINCT UPPER(T.DEPENDENTE) AS NOME,
        REPLACE(REPLACE(REPLACE(T.CPF_DEPENDENTE, '.', ''), '-', ''), '/', '') AS CPF_DEP
    FROM
        DADOS_DEPENDENTES_E_TITULARES T
    WHERE
        T.CPF_DEPENDENTE IS NOT NULL
    """

# SQL to collect all CPFs from oimark
SQL_OIMARK_CPFS = """
    SELECT 
        CUSTOMER,
        REPLACE(REPLACE(REPLACE(t.CPF, '.', ''), '-', ''), '/', '') AS CPF
    FROM 
        FT_OIMARK_CRIE_CLIENTES t
    WHERE 
        T.DATA_INTEGRA = (SELECT MAX(DATA_INTEGRA) FROM FT_OIMARK_CRIE_CLIENTES)
        AND STATUS = 'Concluído'
        AND DATA BETWEEN TO_DATE('01/12/2024', 'DD/MM/RRRR') AND SYSDATE
        AND CPF IS NOT NULL
        AND CUSTOMER IS NOT NULL
    """

# SQL to collect all CPFs from eyal
SQL_EYAL_CPFS = """
    SELECT
        P.NOME,
        P.CPF
    FROM
        paciente p
    INNER JOIN
        paciente_cartao c
    ON 
        P.COD_PACIENTE = C.COD_PACIENTE
    WHERE 
        D_INADIMPLENTE IS NULL
        AND D_INATIVO IS NULL
"""

# SQL to collect all CPFs from RH
SQL_COLLABORATORS_CPFS = """
    SELECT DISTINCT 
        NOME, 
        CPF
    FROM 
        DADOS_QUADRO_GERAL
    WHERE
        NOME IS NOT NULL
        AND CPF IS NOT NULL
"""