import client from './client';

export const getExecutions = (params) => client.get('/executions', { params });
export const getExecution = (id) => client.get(`/executions/${id}`);
export const approveExecution = (id) => client.post(`/executions/${id}/approve`);
export const rejectExecution = (id, reason) => client.post(`/executions/${id}/reject`, { reason });
export const retryExecution = (id) => client.post(`/executions/${id}/retry`);
