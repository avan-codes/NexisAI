import client from './client';

export const getMe = async () => {
  const res = await client.get('/auth/me');
  return res.data;
};

export const loginWithToken = async (token) => {
  const res = await client.get('/auth/me', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};