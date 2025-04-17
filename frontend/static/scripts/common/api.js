export function apiPost(url, data) {
  return fetch(url, {
    method: "POST",
    credentials: "include", // this includes cookies/session
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  }).then(res => res.json());
}

export function apiGet(url) {
  return fetch(url, {
    credentials: "include"
  }).then(res => res.json());
}

export function apiPut(url, data) {
  return fetch(url, {
    method: "PUT",
    credentials: "include",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  }).then(res => res.json());
}


export function apiDelete(url, data = null) {
  const options = {
    method: "DELETE",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  return fetch(url, options).then(res => res.json());
}