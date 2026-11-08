// Alamat lama *.workers.dev dialihkan permanen ke domain utama.
const DOMAIN = "sahabat.kangaher.web.id";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname.endsWith(".workers.dev")) {
      url.hostname = DOMAIN;
      url.port = "";
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
