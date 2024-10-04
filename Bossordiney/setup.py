import cx_Freeze

executables = [cx_Freeze.Executable('PedroVoador.py')]

cx_Freeze.setup(
    name="Bossordiney: The cock sucker",
    options={'build_exe': {'packages':['pygame', 'random'],
                           'include_files':['imagens', 'sons', 'fontes']}},
    executables = executables
)