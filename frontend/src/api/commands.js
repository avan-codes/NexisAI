import client from './client';

export const createCommand = (repo_id, text) => client.post('/commands', { repo_id, text });
export const getCommands = (params) => client.get('/commands', { params });