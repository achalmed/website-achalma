// src/scripts/aula-api.js — cliente mínimo de la API del aula con cuenta (web/_aula/api), para la página «Mi aula».
// El token viaja en `Authorization: Bearer` (sin cookies de terceros: cada pub vive en su propio *.netlify.app).
// La sesión (acceso corto + renovación) se guarda en localStorage de ESTE sitio, envuelto en try/catch como
// almacen.js: con el almacenamiento bloqueado la sesión dura lo que la pestaña. Sin URL de API no se usa nunca.

const CLAVE_SESION = 'aula:sesion';
let enMemoria = null;

function leerSesion() {
  try {
    const v = localStorage.getItem(CLAVE_SESION);
    return v ? JSON.parse(v) : enMemoria;
  } catch {
    return enMemoria;
  }
}
function guardarSesion(s) {
  enMemoria = s;
  try {
    if (s) localStorage.setItem(CLAVE_SESION, JSON.stringify(s));
    else localStorage.removeItem(CLAVE_SESION);
  } catch {
    /* sin almacenamiento: queda en memoria */
  }
}

export class ErrorAula extends Error {
  constructor(estado, detalle) {
    const texto = typeof detalle === 'string' ? detalle : detalle?.mensaje || (Array.isArray(detalle) ? 'Datos no válidos.' : 'Error del aula.');
    super(texto);
    this.estado = estado;
    this.detalle = detalle;
  }
}

export function crearCliente(base) {
  const raiz = String(base || '').replace(/\/+$/, '');
  let renovando = null;

  async function pedir(ruta, { metodo = 'GET', cuerpo, auth = true, crudo = false, reintento = true } = {}) {
    const cabeceras = {};
    const sesion = leerSesion();
    if (auth && sesion?.acceso) cabeceras.Authorization = `Bearer ${sesion.acceso}`;
    let body;
    if (cuerpo instanceof FormData) body = cuerpo;
    else if (cuerpo !== undefined) {
      cabeceras['Content-Type'] = 'application/json';
      body = JSON.stringify(cuerpo);
    }
    let r;
    try {
      r = await fetch(raiz + ruta, { method: metodo, headers: cabeceras, body, credentials: 'omit', mode: 'cors' });
    } catch {
      throw new ErrorAula(0, 'El aula no responde ahora (la laptop que la sirve puede estar apagada). Inténtalo más tarde.');
    }
    if (r.status === 401 && auth && reintento && sesion?.renovacion) {
      if (await renovar()) return pedir(ruta, { metodo, cuerpo, auth, crudo, reintento: false });
    }
    if (!r.ok) {
      let detalle = r.statusText;
      try { detalle = (await r.json()).detail ?? detalle; } catch { /* sin cuerpo */ }
      throw new ErrorAula(r.status, detalle);
    }
    if (crudo) return r;
    return r.status === 204 ? null : r.json();
  }

  async function renovar() {
    renovando ??= (async () => {
      const s = leerSesion();
      try {
        const t = await pedir('/cuentas/renovar', { metodo: 'POST', cuerpo: { renovacion: s.renovacion }, auth: false });
        guardarSesion({ ...s, acceso: t.acceso, renovacion: t.renovacion });
        return true;
      } catch {
        guardarSesion(null);
        return false;
      } finally {
        renovando = null;
      }
    })();
    return renovando;
  }

  const abrir = (datos) => {
    guardarSesion({ acceso: datos.acceso, renovacion: datos.renovacion, usuario: datos.usuario });
    return datos.usuario;
  };

  return {
    sesion: () => leerSesion(),
    privacidad: () => pedir('/privacidad', { auth: false }),
    iniciarSesion: async (correo, clave) => abrir(await pedir('/cuentas/sesion', { metodo: 'POST', cuerpo: { correo, clave }, auth: false })),
    registrarse: async (datos) => abrir(await pedir('/cuentas/registro', { metodo: 'POST', cuerpo: datos, auth: false })),
    async salir() {
      const s = leerSesion();
      guardarSesion(null);
      if (s?.renovacion) {
        try { await pedir('/cuentas/salir', { metodo: 'POST', cuerpo: { renovacion: s.renovacion }, auth: false }); } catch { /* ya salió */ }
      }
    },
    yo: () => pedir('/cuentas/yo'),
    /** Cambia la contraseña; el servidor cierra todas las sesiones, así que se vuelve a entrar con la nueva. */
    async cambiarClave(correo, actual, nueva) {
      await pedir('/cuentas/yo', { metodo: 'PATCH', cuerpo: { clave_actual: actual, clave_nueva: nueva } });
      return abrir(await pedir('/cuentas/sesion', { metodo: 'POST', cuerpo: { correo, clave: nueva }, auth: false }));
    },
    clases: (pub) => pedir(`/clases${pub ? `?pub=${encodeURIComponent(pub)}` : ''}`),
    inscribirse: (codigo) => pedir('/clases/inscribirse', { metodo: 'POST', cuerpo: { codigo } }),
    anuncios: (id) => pedir(`/clases/${id}/anuncios`),
    tareas: (id) => pedir(`/clases/${id}/tareas`),
    examenes: (id) => pedir(`/clases/${id}/examenes`),
    notas: (id) => pedir(`/clases/${id}/notas`),
    /** Une el progreso local con el del servidor y devuelve la unión (la fecha más antigua de cada lección). */
    sincronizarProgreso: (pub, local) => pedir(`/progreso/${encodeURIComponent(pub)}`, { metodo: 'PUT', cuerpo: { completadas: local } }),
    exportarDatos: () => pedir('/cuentas/yo/datos'),
    async borrarCuenta(clave) {
      await pedir('/cuentas/yo', { metodo: 'DELETE', cuerpo: { clave } });
      guardarSesion(null);
    },
  };
}
