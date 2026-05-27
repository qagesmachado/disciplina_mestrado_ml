# disciplina_ml_privado

Dois ambientes virtuais **isolados** (não misturar dependências):

| Venv | Uso | Requirements |
| --- | --- | --- |
| `venv_yolo_5` | YOLOv5 — E01, REF | `requirements-yolov5.txt` ou `requirements.txt` |
| `venv_yolo_ultralytics` | YOLOv8+ — E02 | `requirements-ultralytics.txt` |

Crie cada venv separadamente. **Não** instale `ultralytics` no `venv_yolo_5`.

## Pré-requisitos

- **Python 3.10+** (3.10 é o mais seguro com o meta do wheel `yolov5` no PyPI; em máquinas mais novas, versões posteriores podem funcionar se o `pip` achar wheels).
  - No entanto funciona no Python 3.14.4
- `pip` atualizado: `python -m pip install -U pip`.

## 1. Criar o `venv_yolo_5`

Na raiz do repositório:

```bash
python -m venv venv_yolo_5
```

## 2. Ativar o ambiente

**Windows (PowerShell):**

```powershell
.\venv_yolo_5\Scripts\Activate.ps1
```

Se aparecer erro de política de execução:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv_yolo_5\Scripts\Activate.ps1
```

**Windows (cmd):**

```cmd
venv_yolo_5\Scripts\activate.bat
```

**Linux / macOS:**

```bash
source venv_yolo_5/bin/activate
```

O prompt deve mostrar algo como `(venv_yolo_5)`.

## 3. Instalar dependências

Com o venv ativado:

```bash
python -m pip install -r requirements.txt
```

O `yolov5` instala muitas dependências transitivas (por exemplo `opencv-python`, `pandas`, `ultralytics`, `scipy`, `tensorboard`, etc.).

## 4. Verificação

```bash
python -c "import yolov5, torch; print('OK', torch.__version__)"
```

## 5. Ambiente Ultralytics (E02 YOLOv8)

```powershell
.\experiments\YOLO_V8\setup_venv_ultralytics.ps1
.\experiments\YOLO_V8\run_yolov8_pig.ps1
```

## 6. Scripts (com o venv ativo)

- **Experimentos TCD:** [experiments/README.md](experiments/README.md) — pig fixo, E01 + E02 + REF
- `.\experiments\YOLO_V5\run_pig_baseline.ps1` — YOLOv5: E01 + REF
- `.\experiments\YOLO_V8\run_yolov8_pig.ps1` — YOLOv8: E02
- `python experiments/YOLO_V5/scripts/validar.py REF`
- `python analisar_leitoes_por_imagem.py` -- estatísticas e gráficos
- `python draw_yolo_boxes_v3.py --help` -- desenhar caixas nas imagens

## PyTorch com GPU (opcional)

O `pip` padrão costuma instalar **CPU**. Para **NVIDIA/CUDA**, siga a página oficial do PyTorch: [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/) e instale o par `torch` / `torchvision` compatível com a sua GPU/CUDA, com o venv ativado.

## 7. Desativar o venv

```bash
deactivate
```

