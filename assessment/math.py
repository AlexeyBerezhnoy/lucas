import scipy
import scipy.stats


def math_func():
    """

    table = [[1, 2],
             [2, 3]]

    |                | Первое качество | Второе качество |
    | Первый эксперт |       2         |       3         |
    | Второй эксперт |       2         |       4         |

    """
    table = [[10, 9, 7, 5, 9],
             [9, 8, 8, 6, 8],
             [10, 9, 8, 4, 9]]
    # 1. Переводим оценки группы экспертов из баллов в ранги.
    # Первому рангу будет соответствовать наибольшая оценка в баллах.
    rank_table = scipy.array([len(a)+1 - scipy.stats.rankdata(a) for a in table])
    print(rank_table)
    # 2. При обработке оценок, выданных экспертами в рангах, должна
    # соблюдаться нормировка рангов, то есть сумма рангов должна быть равна сумме
    # членов натурального ряда
    True
    # 3. Вычисляем сумму рангов по каждому из ПВК
    sum_rank_for_q = scipy.array([scipy.sum(a) for a in scipy.rot90(rank_table, k=-1)])
    print(sum_rank_for_q)
    # 4. Получаем общую сумму рангов по всей матрице
    sum_all_rank = scipy.sum(sum_rank_for_q)
    print(sum_all_rank)
    # 5. Находим по формуле среднего арифметического коллективное мнение
    # группы экспертов.
    average_a = scipy.array([scipy.average(a) for a in scipy.rot90(rank_table, k=-1)])
    print(average_a)
    # 6. Вычисляем среднее пофакторное значение суммы рангов.
    m, n = rank_table.shape
    average_value_sum_r = m * (n + 1) / 2
    print(average_value_sum_r)
    # 7. Находим фактические отклонения пофакторных сумм рангов от
    # среднего значения.
    actual_deviation = sum_rank_for_q - average_value_sum_r
    print(actual_deviation)
    # 8. Вычисляем квадраты фактических отклонений пофакторных сумм
    # рангов от общего среднего
    square_actual_deviation = actual_deviation ** 2
    print(square_actual_deviation)
    # 9. Суммируем квадраты отклонений, находим
    sum_square = scipy.sum(square_actual_deviation)
    print(sum_square)
    # 10. Вычисляем максимально возможное значение суммы квадратов
    # отклонений оценок по каждому из ПВК от общей средней
    max_sum_square = m**2 * (n**3 - n) / 12
    print(max_sum_square)
    # 11. Находим выборочное значение коэффициента конкордации Кендэлла.
    W = sum_square/max_sum_square
    print(W)
    # 12. Вычисляем выборочное значение хи-квадрат Пирсона
    chi2 = W * m *(n - 1)
    print(chi2)
    # 13. Проверка согласованности показаний всей группы экспертов с
    # помощью коэффициента конкордации Кендэлла производится согласно
    # следующему альтернативному соглашению:

    pass
