const form = document.querySelector('#consulta');
const title = document.querySelector('#titulo');
const state = document.querySelector('#estado');
const output = document.querySelector('#resposta');
const details = document.querySelector('#detalhes');
const unit = document.querySelector('#unidade');
const responsible = document.querySelector('#responsavel');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  title.textContent = 'Consultando…';
  state.textContent = '';
  output.textContent = '';
  details.hidden = true;

  try {
    const id = document.querySelector('#recurso').value.trim();

    if (!id) {
      throw new Error('Informe o identificador do recurso.');
    }

    const response = await fetch(
      '/api/v2/recursos/' + encodeURIComponent(id)
    );
    const payload = await response.json();

    output.textContent = JSON.stringify(payload, null, 2);

    if (!response.ok) {
      const code = payload?.erro?.codigo || 'ERRO_HTTP';
      throw new Error(
        `HTTP ${response.status} · ${code}`
      );
    }

    for (const field of [
      'id',
      'nome',
      'status',
      'unidade',
      'responsavel'
    ]) {
      if (
        typeof payload[field] !== 'string' ||
        !payload[field].trim()
      ) {
        throw new Error(
          'Resposta sem campo obrigatório válido: ' + field
        );
      }
    }

    title.textContent = payload.nome;
    state.textContent = `${payload.id} · ${payload.status}`;
    unit.textContent = payload.unidade;
    responsible.textContent = payload.responsavel;
    details.hidden = false;
  } catch (error) {
    title.textContent = 'Não foi possível concluir a consulta';
    state.textContent = error.message;
  }
});
