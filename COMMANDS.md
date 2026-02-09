# Comandos úteis para o projeto Lottery Adviser

## Backend

### Desenvolvimento (acessível na rede local)

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

### Desenvolvimento (apenas localhost)

```bash
cd backend
uvicorn app.main:app --reload --port 5000
```

### Migração de dados

```bash
cd backend
python scripts/migrate_data.py
```

## Frontend

### Iniciar servidor de desenvolvimento

```bash
cd frontend
npm start
```

### Atualizar IP da rede (quando mudar)

```bash
cd frontend
npm run update-ip
```

## Notas Importantes

- **Backend**: Use `--host 0.0.0.0` para permitir conexões de dispositivos móveis na mesma rede
- **Frontend**: Sempre reinicie o Expo após atualizar o IP no `.env`
- **Porta**: Backend roda na porta 5000 (não 8000) para evitar conflitos
