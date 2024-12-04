export const state = {
  token: localStorage.getItem('token') || null,
};

export const mutations = {
  SET_TOKEN(state, token) {
    state.token = token;
    localStorage.setItem('token', token);
  },
  REMOVE_TOKEN(state) {
    state.token = null;
    localStorage.removeItem('token');
  },
};

export const actions = {
  login({ commit }, token) {
    commit('SET_TOKEN', token);
  },
  logout({ commit }) {
    commit('REMOVE_TOKEN');
  },
};
