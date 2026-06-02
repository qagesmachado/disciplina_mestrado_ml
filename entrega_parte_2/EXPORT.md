# Exportação para o Moodle

Arquivos-fonte prontos. Exporte manualmente (Pandoc não instalado nesta máquina).

## Relatório PDF

**Fonte:** [rascunho_relatorio.md](rascunho_relatorio.md)

**Nome de entrega:** `Etapa2 GustavoMachado Relatorio.pdf`

Opções:

1. Copiar markdown para Word/Google Docs → incluir figuras de `../experiments/shared/outputs/figures/` (métricas `G1_*.png`; tempo `G2_ms_per_image.png`) → Exportar PDF
2. Instalar [Pandoc](https://pandoc.org/) e rodar:

```powershell
pandoc entrega_parte_2/rascunho_relatorio.md -o "Etapa2 GustavoMachado Relatorio.pdf"
```

## Fluxograma PNG

**Fonte:** [fluxograma.md](fluxograma.md)

1. Abrir https://mermaid.live
2. Colar o bloco mermaid
3. Export PNG → `Etapa2 GustavoMachado Fluxograma.png`

## Slides

**Fonte:** [roteiro_slides.md](roteiro_slides.md)

Montar no PowerPoint/Google Slides (~10 slides). Incluir:

- Fluxograma exportado
- Tabela E01–E03 de [comparacao_pig_baseline.md](../experiments/shared/outputs/comparacao_pig_baseline.md)
- Gráficos de `../experiments/shared/outputs/figures/` (métricas `G1_*.png`; tempo `G2_*.png`)

**Nome sugerido:** `Etapa2 GustavoMachado Slides.pdf`

## Checklist final

- [ ] Relatório PDF
- [ ] Fluxograma PNG (incorporado ao relatório ou separado)
- [ ] Slides PDF/PPTX
- [ ] Upload no Moodle
