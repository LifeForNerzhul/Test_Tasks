from ------Pages import SearchHelper


def test_check_sensor_ram_v30(browser):
    -------_help_page = SearchHelper(browser)
    -------_help_page.go_to_site()
    -------_help_page.help_page()
    -------_help_page.product_page()
    -------_help_page.check_target()
    -------_help_page.check_version()


def test_check_sensor_ram_v40(browser):
    -------_help_page = SearchHelper(browser, loc_version='4.0', loc_target='RAM: 8 GB, and an additional 2 GB for '
                                                                           'each monitoring point on this computer')
    ------_help_page.go_to_site()
    ------_help_page.help_page()
    ------_help_page.product_page()
    ------_help_page.check_target()
    ------_help_page.check_version()


def test_check_sensor_ram_v40_rus(browser):
    ------_help_page = SearchHelper(browser, loc_version='4.0',
                                    loc_block_name='О ------------------------ for Networks',
                                    loc_sub_block_name='Аппаратные и программные требования',
                                    loc_target='объем оперативной памяти: 8 ГБ и по 2 ГБ '
                                               'для каждой точки мониторинга на этом '
                                               'компьютере;')
    ------_help_page.go_to_site()
    ------_help_page.help_page()
    ------_help_page.switch_lang()
    ------_help_page.product_page()
    ------_help_page.check_target()
    ------_help_page.check_version()
