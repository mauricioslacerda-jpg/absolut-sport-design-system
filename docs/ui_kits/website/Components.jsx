// ABSOLUT Sport — Shared UI Components
// ui_kits/website/Components.jsx

// ─── THEME ──────────────────────────────────────────────────────────────────
const ThemeContext = React.createContext({ dark: false, toggle: () => {} });

const LIGHT = {
  bgBase:       '#FAFAFA', bgSurface: '#FFFFFF', bgCard: '#F0F0F0',
  bgCardHover:  '#E8E8E8', bgHero: 'linear-gradient(135deg, #EAF2FB 0%, #FAFAFA 100%)',
  bgStrip:      '#FFFFFF', bgDark: '#0D0D0D',
  fgPrimary:    '#0D0D0D', fgSecondary: '#333333', fgMuted: '#7A7A7A',
  fgInverse:    '#FFFFFF',
  accent:       '#155F97', accentHover: '#0F4A75', accentHL: '#2857F7',
  border:       'rgba(0,0,0,0.08)', borderStrong: 'rgba(0,0,0,0.15)',
  cardShadow:   '0 2px 12px rgba(0,0,0,0.08)',
  navBg:        'rgba(250,250,250,0.97)',
  navBorder:    'rgba(0,0,0,0.08)',
};
const DARK = {
  bgBase:       '#0D0D0D', bgSurface: '#141414', bgCard: '#1A1A1A',
  bgCardHover:  '#252525', bgHero: 'linear-gradient(135deg, #0D0D0D 0%, #0a1520 50%, #0D0D0D 100%)',
  bgStrip:      '#141414', bgDark: '#0D0D0D',
  fgPrimary:    '#FFFFFF', fgSecondary: '#C4C4C4', fgMuted: '#7A7A7A',
  fgInverse:    '#FFFFFF',
  accent:       '#1E7ABE', accentHover: '#155F97', accentHL: '#2857F7',
  border:       'rgba(255,255,255,0.08)', borderStrong: 'rgba(255,255,255,0.15)',
  cardShadow:   '0 4px 24px rgba(0,0,0,0.4)',
  navBg:        'rgba(13,13,13,0.97)',
  navBorder:    'rgba(255,255,255,0.07)',
};

// ─── LOGO ────────────────────────────────────────────────────────────────────
const LogoMark = ({ size = 36, dark = false }) => (
  <img
    src={dark ? "../../assets/logo-azul-branco.svg" : "../../assets/logo-azul-preto.svg"}
    alt="ABSOLUT Sport"
    style={{ height: size, objectFit: "contain" }}
  />
);

const Logo = ({ size = "md" }) => {
  const { dark } = React.useContext(ThemeContext);
  const h = size === "sm" ? 28 : size === "lg" ? 52 : 38;
  const src = dark ? "../../assets/logo-azul-branco.svg" : "../../assets/logo-azul-preto.svg";
  return <img src={src} alt="ABSOLUT Sport" style={{ height: h, objectFit: "contain" }} />;
};

// ─── THEME TOGGLE ────────────────────────────────────────────────────────────
const ThemeToggle = () => {
  const { dark, toggle } = React.useContext(ThemeContext);
  const t = dark ? DARK : LIGHT;
  return (
    <button onClick={toggle} style={{
      background: t.bgCard, border: `1px solid ${t.border}`,
      borderRadius: 100, padding: '6px 14px', cursor: 'pointer',
      display: 'flex', alignItems: 'center', gap: 7,
      fontSize: 12, fontWeight: 600, color: t.fgSecondary,
      fontFamily: "'Barlow', sans-serif", transition: 'all 0.2s',
    }}>
      {dark ? '☀️' : '🌙'} {dark ? 'Light' : 'Dark'}
    </button>
  );
};

// ─── BADGE ───────────────────────────────────────────────────────────────────
const Badge = ({ children, variant = "blue" }) => {
  const variants = {
    blue:    { bg: 'rgba(21,95,151,0.12)',  color: '#155F97', border: 'rgba(21,95,151,0.25)' },
    gold:    { bg: 'rgba(201,168,76,0.15)', color: '#C9A84C', border: 'rgba(201,168,76,0.3)' },
    white:   { bg: 'rgba(255,255,255,0.12)',color: '#fff',    border: 'rgba(255,255,255,0.2)' },
    success: { bg: 'rgba(34,197,94,0.12)',  color: '#22C55E', border: 'rgba(34,197,94,0.25)' },
  };
  const v = variants[variant] || variants.blue;
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 5,
      padding: '3px 10px', borderRadius: 100,
      background: v.bg, color: v.color, border: `1px solid ${v.border}`,
      fontSize: 10, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase',
      fontFamily: "'Barlow', sans-serif",
    }}>{children}</span>
  );
};

// ─── BUTTON ──────────────────────────────────────────────────────────────────
const Button = ({ children, variant = "primary", size = "md", onClick, style: sx = {} }) => {
  const { dark } = React.useContext(ThemeContext);
  const t = dark ? DARK : LIGHT;
  const [hov, setHov] = React.useState(false);
  const base = {
    fontFamily: "'SoulCraft', 'Barlow Condensed', sans-serif",
    fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase',
    border: 'none', borderRadius: 4, cursor: 'pointer',
    transition: 'all 0.15s ease-out', ...sx,
  };
  const sizes = { sm: { padding: '8px 16px', fontSize: 12 }, md: { padding: '12px 28px', fontSize: 15 }, lg: { padding: '16px 36px', fontSize: 18 } };
  const variants = {
    primary:   { background: hov ? t.accentHover : t.accent, color: '#fff' },
    secondary: { background: 'transparent', color: t.fgPrimary, border: `1.5px solid ${t.borderStrong}` },
    gold:      { background: '#C9A84C', color: '#0D0D0D' },
    ghost:     { background: 'transparent', color: t.fgMuted, textDecoration: 'underline', textUnderlineOffset: 3 },
  };
  return (
    <button style={{ ...base, ...sizes[size], ...variants[variant] }}
      onMouseEnter={() => setHov(true)} onMouseLeave={() => setHov(false)}
      onClick={onClick}>{children}</button>
  );
};

// ─── NAVBAR ──────────────────────────────────────────────────────────────────
const Navbar = ({ currentPage, onNavigate }) => {
  const { dark } = React.useContext(ThemeContext);
  const t = dark ? DARK : LIGHT;
  return (
    <nav style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '0 48px', height: 68,
      background: t.navBg, borderBottom: `1px solid ${t.navBorder}`,
      position: 'sticky', top: 0, zIndex: 200,
    }}>
      <Logo />
      <div style={{ display: 'flex', gap: 28 }}>
        {['Eventos', 'Libertadores', 'Sudamericana', 'Sobre Nós'].map(item => (
          <a key={item} onClick={() => onNavigate && onNavigate(item)} style={{
            fontSize: 13, fontWeight: 600, letterSpacing: '0.05em', textTransform: 'uppercase',
            color: currentPage === item ? t.accent : t.fgMuted,
            cursor: 'pointer', textDecoration: 'none',
            borderBottom: currentPage === item ? `2px solid ${t.accent}` : '2px solid transparent',
            paddingBottom: 2, transition: 'all 0.15s',
          }}>{item}</a>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
        <ThemeToggle />
        <Button onClick={() => onNavigate && onNavigate('Pacotes')}>Comprar Pacote</Button>
      </div>
    </nav>
  );
};

// ─── STAT STRIP ──────────────────────────────────────────────────────────────
const StatStrip = () => {
  const { dark } = React.useContext(ThemeContext);
  const t = dark ? DARK : LIGHT;
  return (
    <div style={{ display: 'flex', background: t.bgStrip, borderTop: `1px solid ${t.border}`, borderBottom: `1px solid ${t.border}` }}>
      {[
        { val: '+5oo', label: 'Eventos anuais' },
        { val: '+1oK', label: 'Viagens por ano' },
        { val: '+3o',  label: 'Parceiros globais' },
        { val: '14+',  label: 'Anos de experiência' },
      ].map((s, i) => (
        <div key={i} style={{ flex: 1, padding: '24px 0', textAlign: 'center', borderRight: i < 3 ? `1px solid ${t.border}` : 'none' }}>
          <div style={{ fontFamily: "'SoulCraft', 'Barlow Condensed', sans-serif", fontSize: 36, fontWeight: 900, color: t.accent, lineHeight: 1 }}>{s.val}</div>
          <div style={{ fontSize: 12, color: t.fgMuted, marginTop: 6, fontWeight: 500 }}>{s.label}</div>
        </div>
      ))}
    </div>
  );
};

// ─── EVENT CARD ──────────────────────────────────────────────────────────────
const EventCard = ({ event, onSelect }) => {
  const { dark } = React.useContext(ThemeContext);
  const t = dark ? DARK : LIGHT;
  const [hov, setHov] = React.useState(false);
  return (
    <div
      onMouseEnter={() => setHov(true)} onMouseLeave={() => setHov(false)}
      onClick={() => onSelect && onSelect(event)}
      style={{
        background: t.bgCard, borderRadius: 8, overflow: 'hidden',
        border: `1px solid ${hov ? t.accent : t.border}`,
        cursor: 'pointer', transition: 'all 0.2s ease-out',
        transform: hov ? 'scale(1.02)' : 'scale(1)',
        boxShadow: hov ? `0 8px 32px rgba(21,95,151,0.2)` : t.cardShadow,
      }}>
      <div style={{
        height: 150, position: 'relative',
        background: `linear-gradient(135deg, ${event.color1} 0%, ${event.color2} 100%)`,
      }}>
        <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 55%)' }} />
        <div style={{ position: 'absolute', top: 12, right: 12 }}><Badge variant="blue">Oficial</Badge></div>
        <div style={{
          position: 'absolute', bottom: 14, left: 16,
          fontFamily: "'SoulCraft', 'Barlow Condensed', sans-serif", fontSize: 20, fontWeight: 800,
          textTransform: 'uppercase', color: '#fff', lineHeight: 1.1,
        }}>{event.name}</div>
      </div>
      <div style={{ padding: 16 }}>
        <div style={{ display: 'flex', gap: 14, fontSize: 12, color: t.fgMuted, marginBottom: 12 }}>
          <span>📍 {event.location}</span><span>📅 {event.date}</span>
        </div>
        <div style={{ fontFamily: 'Barlow, sans-serif', fontSize: 11, color: t.fgMuted }}>A partir de</div>
        <div style={{ fontFamily: "'SoulCraft', 'Barlow Condensed', sans-serif", fontSize: 26, fontWeight: 800, color: dark ? '#FFFFFF' : t.accent, lineHeight: 1 }}>
          {event.price} <span style={{ fontSize: 14, color: t.fgMuted, fontFamily: "'Barlow', sans-serif", fontWeight: 400 }}>/pessoa</span>
        </div>
        <button style={{
          display: 'block', width: '100%', marginTop: 14,
          background: t.accent, color: '#fff', border: 'none',
          padding: '10px', fontFamily: "'SoulCraft', 'Barlow Condensed', sans-serif",
          fontSize: 14, fontWeight: 700, letterSpacing: '0.08em',
          textTransform: 'uppercase', borderRadius: 4, cursor: 'pointer',
        }}>Ver Pacotes</button>
      </div>
    </div>
  );
};

// ─── FEATURE LIST ────────────────────────────────────────────────────────────
const FeatureList = ({ items }) => {
  const { dark } = React.useContext(ThemeContext);
  const t = dark ? DARK : LIGHT;
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {items.map((item, i) => (
        <div key={i} style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
          <div style={{
            width: 22, height: 22, background: `rgba(21,95,151,0.1)`, borderRadius: '50%',
            flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', marginTop: 1,
          }}>
            <svg width="10" height="8" viewBox="0 0 10 8" fill="none">
              <path d="M1 4L4 7L9 1" stroke={t.accent} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <div style={{ fontSize: 14, color: t.fgSecondary, lineHeight: 1.5 }}>{item}</div>
        </div>
      ))}
    </div>
  );
};

// ─── FOOTER ──────────────────────────────────────────────────────────────────
const Footer = () => {
  const { dark } = React.useContext(ThemeContext);
  const t = dark ? DARK : LIGHT;
  return (
    <footer style={{ background: dark ? '#0D0D0D' : '#0D0D0D', borderTop: '1px solid rgba(255,255,255,0.07)', padding: '48px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', maxWidth: 1200, margin: '0 auto', gap: 40 }}>
        <div>
          <img src="../../assets/logo-azul-branco.svg" alt="ABSOLUT Sport" style={{ height: 38, objectFit: 'contain' }} />
          <p style={{ fontSize: 13, color: '#555', marginTop: 14, maxWidth: 260, lineHeight: 1.6 }}>
            A única agência oficial de pacotes para as Finais da CONMEBOL Libertadores™ e Sudamericana™.
          </p>
          <div style={{ marginTop: 16 }}><Badge variant="blue">Agência Oficial CONMEBOL</Badge></div>
        </div>
        {[
          { title: 'Eventos', links: ['Libertadores 2025', 'Sudamericana 2025', 'Formula 1', 'NFL', 'Tênis'] },
          { title: 'Empresa', links: ['Sobre Nós', 'Parceiros', 'Imprensa', 'Contato'] },
          { title: 'Contato', links: ['Rio de Janeiro 🇧🇷', 'Frankfurt 🇩🇪', 'Los Angeles 🇺🇸', 'WhatsApp'] },
        ].map(col => (
          <div key={col.title}>
            <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.15em', textTransform: 'uppercase', color: '#555', marginBottom: 14 }}>{col.title}</div>
            {col.links.map(l => <div key={l} style={{ fontSize: 13, color: '#7A7A7A', marginBottom: 8, cursor: 'pointer' }}>{l}</div>)}
          </div>
        ))}
      </div>
      <div style={{ maxWidth: 1200, margin: '32px auto 0', paddingTop: 24, borderTop: '1px solid rgba(255,255,255,0.06)', display: 'flex', justifyContent: 'space-between' }}>
        <div style={{ fontSize: 12, color: '#555' }}>© 2025 ABSOLUT Sport. Todos os direitos reservados.</div>
        <div style={{ fontSize: 12, color: '#555' }}>Rio de Janeiro · Frankfurt · Los Angeles · Buenos Aires</div>
      </div>
    </footer>
  );
};

Object.assign(window, { ThemeContext, LIGHT, DARK, Logo, LogoMark, ThemeToggle, Badge, Button, Navbar, StatStrip, EventCard, FeatureList, Footer });
