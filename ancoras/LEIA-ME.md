# Âncoras de integridade — SIGAB / QUANTOCA (AvHoFlu Rio Tocantins, H-12)

Todo dia às 23:00 (Belém/Brasília) uma tarefa automática do GitHub — que roda **fora** do
banco de dados — grava aqui a "impressão digital" (hash) de todos os registros até aquele
momento, e carimba esse arquivo no **OpenTimestamps**, um registro público no Bitcoin que
ninguém consegue alterar ou apagar, nem o dono do sistema.

Cada arquivo `AAAA/AAAA-MM-DD.json` tem:
- `movimentos`: total de registros de movimentação do QUANTOCA, se a cadeia está íntegra,
  o número do último registro (`cabeca_seq`) e o hash dele (`cabeca_hash`);
- `rastro`: o mesmo para o rastro de acessos (quem gravou o quê, de onde);
- `sha256_deste_registro`: o resumo do próprio arquivo.

O arquivo `.ots` ao lado é o carimbo público.

## Como um perito confere, sem depender de ninguém

1. Instale o cliente gratuito: `pip install opentimestamps-client`.
2. Baixe o `.json` e o `.ots` do dia e rode `ots verify AAAA-MM-DD.json.ots`.
   Ele mostra em que data o arquivo já existia, segundo o Bitcoin.
3. No laudo de integridade (PDF gerado no QUANTOCA) estão os registros do período, cada um
   com o texto exato que entra no hash. Calcule o SHA-256 de cada texto: tem de dar o hash
   impresso, e cada registro aponta para o hash do anterior até chegar à `cabeca_hash`
   carimbada aqui. Se um único caractere de um registro tivesse sido mudado depois, a conta
   não fecharia.
