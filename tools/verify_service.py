"""Executor pronto para validação de um serviço; o trabalho do laboratório é YAML."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
RUN_TESTS = r'''
import json, sys, unittest
suite = unittest.defaultTestLoader.discover(sys.argv[1], pattern='test_*.py')
count = suite.countTestCases()
if count == 0:
    print('ERRO: nenhum teste encontrado.', file=sys.stderr)
    sys.exit(2)
result = unittest.TextTestRunner(verbosity=2).run(suite)
print(json.dumps({'testes_descobertos': count, 'testes_executados': result.testsRun}))
sys.exit(0 if result.wasSuccessful() else 1)
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-path', required=True)
    parser.add_argument('--test-path', required=True)
    parser.add_argument('--cenario', default=os.environ.get('LAB_CENARIO', 'normal'),
                        choices=['normal', 'falha'])
    args = parser.parse_args()
    if args.cenario not in ('normal', 'falha'):
        parser.error('Cenário inválido')
    project = (ROOT / args.project_path).resolve()
    services = (ROOT / 'services').resolve()
    if project.parent != services or not project.is_dir():
        parser.error('project-path precisa apontar para um serviço existente em services/')
    test_path = (project / args.test_path).resolve()
    if not test_path.is_relative_to(project) or not test_path.is_dir():
        parser.error('test-path precisa existir dentro do serviço')
    result = subprocess.run([sys.executable, '-c', RUN_TESTS,
                             str(test_path.relative_to(project))], cwd=project)
    git = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                         capture_output=True, text=True)
    sha = git.stdout.strip() if git.returncode == 0 else 'sem-revisao-git'
    forced = args.cenario == 'falha'
    code = result.returncode or (1 if forced else 0)
    report = {'servico': project.name, 'project_path': args.project_path,
              'test_path': args.test_path, 'python': sys.version.split()[0],
              'commit': sha, 'cenario': args.cenario,
              'testes_exit_code': result.returncode, 'falha_controlada': forced,
              'exit_code': code}
    destination = ROOT / 'outputs' / project.name
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'validacao.json').write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False), flush=True)
    if forced:
        print('SONDA: reprovação controlada; não é um defeito da aplicação.', file=sys.stderr)
    return code


if __name__ == '__main__':
    raise SystemExit(main())
