import scipy
import scipy.stats
from openpyxl import Workbook
from openpyxl import load_workbook
import xlrd as xlrd


def math_func(table):
    """

    table = [[1, 2],
             [2, 3]]

    |                | Первое качество | Второе качество |
    | Первый эксперт |       2         |       3         |
    | Второй эксперт |       2         |       4         |

    """
    # table = [[10, 9, 7, 5, 9],
    #          [9, 8, 8, 6, 8],
    #          [10, 9, 8, 4, 9]]
    table = scipy.array(table)
    print(table)

    # 1. Переводим оценки группы экспертов из баллов в ранги.
    # Первому рангу будет соответствовать наибольшая оценка в баллах.
    rank_table = scipy.array([scipy.stats.mstats.rankdata(a) for a in table])
    rank_table = scipy.array(
        [scipy.array([r.shape[0] + 1 - value if value > 0 else 0 for value in r]) for r in rank_table])
    print(rank_table)

    m, n = rank_table.shape  # Количество экспертов, количетво качеств

    # Находим критические точки распределения Пирсона по таблице [5],
    # вычисленные при заданном уровне значимости α = 0,05 и при числе степеней
    # свободы K = n - 1
    print("sdfsdf", n)
    critical_chi = scipy.stats.chi2.isf(0.05, n - 1)

    # 2. При обработке оценок, выданных экспертами в рангах, должна
    # соблюдаться нормировка рангов, то есть сумма рангов должна быть равна сумме
    # членов натурального ряда

    # 3. Вычисляем сумму рангов по каждому из ПВК
    sum_rank_for_q = scipy.array([scipy.sum(a) for a in scipy.rot90(rank_table, k=-1)])

    # 4. Получаем общую сумму рангов по всей матрице
    sum_all_rank = scipy.sum(sum_rank_for_q)

    # 5. Находим по формуле среднего арифметического коллективное мнение
    # группы экспертов.
    average_a = scipy.array([scipy.average(a) for a in scipy.rot90(rank_table, k=-1)])

    # 6. Вычисляем среднее пофакторное значение суммы рангов.
    average_value_sum_r = m * (n + 1) / 2

    # 7. Находим фактические отклонения пофакторных сумм рангов от
    # среднего значения.
    actual_deviation = sum_rank_for_q - average_value_sum_r

    # 8. Вычисляем квадраты фактических отклонений пофакторных сумм
    # рангов от общего среднего
    square_actual_deviation = actual_deviation ** 2

    # 9. Суммируем квадраты отклонений, находим
    sum_square = scipy.sum(square_actual_deviation)

    # 10. Вычисляем максимально возможное значение суммы квадратов
    # отклонений оценок по каждому из ПВК от общей средней
    max_sum_square = m ** 2 * (n ** 3 - n) / 12

    # 11. Находим выборочное значение коэффициента конкордации Кендэлла.
    W = sum_square / max_sum_square

    # 12. Вычисляем выборочное значение хи-квадрат Пирсона
    chi2 = W * m * (n - 1)
    print("chi2", chi2)
    print("critical", critical_chi)
    # 13. Проверка согласованности показаний всей группы экспертов с
    # помощью коэффициента конкордации Кендэлла производится согласно
    # следующему альтернативному соглашению:
    if chi2 >= critical_chi:
        print("yes")
        return False
    else:
        print("no")
        return True


def test_math_func():
    rb = xlrd.open_workbook(filename=r'C:\Users\HP\Documents\my projects\lucas\assessment\test.xls')
    sheet = rb.sheet_by_index(0)
    table = []
    for rownum in range(sheet.nrows):
        rowdata = []
        for colnum in range(sheet.ncols):
            rowdata.append(sheet.cell_value(rownum, colnum))
        table.append(rowdata)
    # table = scipy.rot90(scipy.array(table))
    math_func(table)
