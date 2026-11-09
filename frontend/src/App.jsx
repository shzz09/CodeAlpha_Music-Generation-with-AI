
import { useState } from "react";
import {
  AudioWaveform,
  Music2,
  Library,
  Sparkles,
  Settings,
  Headphones,
  Download,
  Plus,
  Clock3,
  SlidersHorizontal,
  Bell,
  WandSparkles,
  Play,
} from "lucide-react";

import "./App.css";

function App() {
  const [activePage, setActivePage] = useState("Create");
  const [length, setLength] = useState("Medium");
  const [creativity, setCreativity] = useState(1);
  const [notice, setNotice] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [generated, setGenerated] = useState(false);
  const [audioUrl, setAudioUrl] = useState("");

  const lengths = ["Short", "Medium", "Long", "Extended"];

  const handleGenerate = async () => {
    setIsGenerating(true);
    setNotice("");
    setGenerated(false);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          length,
          creativity,
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || "Music generation failed.");
      }

      setAudioUrl(
        `http://127.0.0.1:5000/api/audio?t=${Date.now()}`
      );

      setGenerated(true);
      setNotice("Your music has been generated successfully!");
    } catch (error) {
      setNotice(
        error.message || "Unable to connect to the music generation server."
      );
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="app-shell">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <AudioWaveform size={23} />
          </div>
          <span>
            Melody<span className="brand-accent">AI</span>
          </span>
        </div>

        <div className="workspace-label">WORKSPACE</div>

        <nav className="navigation">
          <button
            className={activePage === "Create" ? "nav-item active" : "nav-item"}
            onClick={() => setActivePage("Create")}
          >
            <WandSparkles size={19} />
            <span>Create</span>
          </button>

          <button
            className={activePage === "Library" ? "nav-item active" : "nav-item"}
            onClick={() => setActivePage("Library")}
          >
            <Library size={19} />
            <span>My Library</span>
          </button>

          <button
            className={activePage === "Discover" ? "nav-item active" : "nav-item"}
            onClick={() => setActivePage("Discover")}
          >
            <Headphones size={19} />
            <span>Discover</span>
          </button>
        </nav>

        <div className="sidebar-bottom">
          <button
            className="nav-item"
            onClick={() => setNotice("Settings will be available soon.")}
          >
            <Settings size={19} />
            <span>Settings</span>
          </button>

          <div className="profile">
            <div className="avatar">M</div>
            <div>
              <div className="profile-name">MelodyAI Studio</div>
              <div className="profile-status">Personal workspace</div>
            </div>
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">
        {/* TOPBAR */}
        <header className="topbar">
          <div className="breadcrumb">
            Studio <span>/</span> {activePage}
          </div>

          <div className="topbar-right">
            <span className="engine-status">
              <span className="status-dot"></span>
              AI Studio
            </span>
            <button className="icon-button" aria-label="Notifications">
              <Bell size={19} />
            </button>
            <div className="top-avatar">M</div>
          </div>
        </header>

        {/* CREATE PAGE */}
        {activePage === "Create" && (
          <>
            <section className="hero">
              <div className="hero-text">
                <div className="eyebrow">
                  <Sparkles size={14} />
                  YOUR CREATIVE SPACE
                </div>

                <h1>
                  Make something
                  <br />
                  <span>extraordinary.</span>
                </h1>

                <p>
                  Turn musical possibilities into melodies.
                  <br />
                  Your next creation starts here.
                </p>
              </div>

              <div className="hero-art">
                <div className="art-circle circle-one"></div>
                <div className="art-circle circle-two"></div>
                <div className="art-circle circle-three"></div>
                <AudioWaveform className="hero-wave" size={100} />
                <div className="floating-note note-one">♪</div>
                <div className="floating-note note-two">♫</div>
              </div>
            </section>

            {/* GENERATOR */}
            <section className="studio-grid">
              <div className="creation-panel">
                <div className="section-heading">
                  <div>
                    <div className="section-title">Create your music</div>
                    <div className="section-subtitle">
                      Customize your generation settings.
                    </div>
                  </div>
                  <div className="sparkle-icon">
                    <Sparkles size={19} />
                  </div>
                </div>

                <div className="field-group">
                  <label>
                    <Clock3 size={16} />
                    TRACK LENGTH
                  </label>

                  <div className="length-options">
                    {lengths.map((item) => (
                      <button
                        key={item}
                        className={
                          length === item
                            ? "length-btn selected"
                            : "length-btn"
                        }
                        onClick={() => setLength(item)}
                        disabled={isGenerating}
                      >
                        {item}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="field-group">
                  <div className="slider-heading">
                    <label>
                      <SlidersHorizontal size={16} />
                      CREATIVITY
                    </label>
                    <span className="slider-value">
                      {creativity.toFixed(1)}
                    </span>
                  </div>

                  <input
                    type="range"
                    min="0.5"
                    max="1.5"
                    step="0.1"
                    value={creativity}
                    onChange={(e) =>
                      setCreativity(Number(e.target.value))
                    }
                    className="creativity-slider"
                    disabled={isGenerating}
                  />

                  <div className="slider-labels">
                    <span>Balanced</span>
                    <span>Experimental</span>
                  </div>
                </div>

                <div className="generation-summary">
                  <div>
                    <span className="summary-label">Selected length</span>
                    <strong>{length}</strong>
                  </div>
                  <div>
                    <span className="summary-label">Creativity</span>
                    <strong>{creativity.toFixed(1)}</strong>
                  </div>
                </div>

                <button
                  className="generate-button"
                  onClick={handleGenerate}
                  disabled={isGenerating}
                >
                  <Sparkles size={18} />
                  {isGenerating ? "Generating Music..." : "Generate Music"}
                </button>

                {notice && (
                  <div className="notice" role="status">
                    {notice}
                  </div>
                )}

                <p className="panel-footnote">
                  Powered by your AI music generation engine.
                </p>
              </div>

              {/* PREVIEW PANEL */}
              <div className="preview-panel">
                <div className="preview-header">
                  <div>
                    <div className="section-title">Music preview</div>
                    <div className="section-subtitle">
                      Your creative output, all in one place.
                    </div>
                  </div>
                  <div className="preview-icon">
                    <Music2 size={21} />
                  </div>
                </div>

                <div className="visualizer">
                  {Array.from({ length: 45 }).map((_, index) => (
                    <div
                      key={index}
                      className="wave-bar"
                      style={{
                        height: `${
                          18 + Math.abs(Math.sin(index * 0.65)) * 95
                        }px`,
                      }}
                    ></div>
                  ))}
                </div>

                {generated ? (
                  <div className="preview-empty">
                    <div className="empty-icon">
                      <AudioWaveform size={25} />
                    </div>

                    <h3>Your melody is ready!</h3>
                    <p>
                      Your AI-generated music is ready to play.
                    </p>

                    <audio
                      key={audioUrl}
                      controls
                      src={audioUrl}
                      style={{
                        width: "100%",
                        marginTop: "16px",
                      }}
                    >
                      Your browser does not support audio playback.
                    </audio>

                    <a
                      href="http://127.0.0.1:5000/api/midi"
                      download="MelodyAI_Generated.mid"
                      className="view-button"
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: "8px",
                        marginTop: "16px",
                        textDecoration: "none",
                      }}
                    >
                      <Download size={16} />
                      Download MIDI
                    </a>
                  </div>
                ) : (
                  <div className="preview-empty">
                    <div className="empty-icon">
                      <AudioWaveform size={25} />
                    </div>
                    <h3>Your next melody awaits</h3>
                    <p>
                      Configure your settings and generate your first track.
                    </p>
                  </div>
                )}

                <div className="preview-footer">
                  <span>
                    <span className="status-dot"></span>
                    {isGenerating
                      ? "Generating..."
                      : generated
                      ? "Track generated"
                      : "Ready to create"}
                  </span>
                  <span>MelodyAI Studio</span>
                </div>
              </div>
            </section>

            {/* LIBRARY */}
            <section className="library-section">
              <div className="library-heading">
                <div>
                  <div className="section-title">Your creations</div>
                  <div className="section-subtitle">
                    Keep all your generated music together.
                  </div>
                </div>

                <button
                  className="view-button"
                  onClick={() => setActivePage("Library")}
                >
                  View library
                </button>
              </div>

              {generated ? (
                <div className="empty-library">
                  <div className="empty-library-icon">
                    <Music2 size={25} />
                  </div>
                  <h3>MelodyAI Generated Track</h3>
                  <p>
                    {length} track · Creativity {creativity.toFixed(1)}
                  </p>
                  <button
                    className="start-button"
                    onClick={() => setActivePage("Library")}
                  >
                    <Library size={16} />
                    View track
                  </button>
                </div>
              ) : (
                <div className="empty-library">
                  <div className="empty-library-icon">
                    <Music2 size={25} />
                  </div>
                  <h3>No tracks yet</h3>
                  <p>Your generated melodies will appear here.</p>
                  <button
                    className="start-button"
                    onClick={() =>
                      window.scrollTo({ top: 0, behavior: "smooth" })
                    }
                  >
                    <Plus size={16} />
                    Start creating
                  </button>
                </div>
              )}
            </section>
          </>
        )}

        {/* LIBRARY PAGE */}
        {activePage === "Library" && (
          <section className="secondary-page">
            <div className="eyebrow">YOUR MUSIC COLLECTION</div>
            <h1>My Library</h1>
            <p>All your generated tracks will be organized here.</p>

            <div className="empty-library">
              {generated ? (
                <>
                  <Music2 size={32} />
                  <h3>MelodyAI Generated Track</h3>
                  <p>
                    {length} track · Creativity {creativity.toFixed(1)}
                  </p>
                  <audio
                    controls
                    src={audioUrl}
                    style={{ width: "100%", marginTop: "15px" }}
                  />
                  <a
                    href="http://127.0.0.1:5000/api/midi"
                    download="MelodyAI_Generated.mid"
                    className="view-button"
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "8px",
                      marginTop: "15px",
                      textDecoration: "none",
                    }}
                  >
                    <Download size={16} />
                    Download MIDI
                  </a>
                </>
              ) : (
                <>
                  <Library size={32} />
                  <h3>Your library is waiting</h3>
                  <p>Generate music to see your tracks here.</p>
                  <button
                    className="start-button"
                    onClick={() => setActivePage("Create")}
                  >
                    <Plus size={16} /> Create music
                  </button>
                </>
              )}
            </div>
          </section>
        )}

        {/* DISCOVER PAGE */}
        {activePage === "Discover" && (
          <section className="secondary-page">
            <div className="eyebrow">EXPLORE YOUR CREATIVITY</div>
            <h1>Discover</h1>
            <p>Explore the possibilities of AI-generated melodies.</p>
            <div className="empty-library">
              <Headphones size={32} />
              <h3>Discover new sounds</h3>
              <p>Your music exploration space.</p>
              <button
                className="start-button"
                onClick={() => setActivePage("Create")}
              >
                <Plus size={16} /> Create music
              </button>
            </div>
          </section>
        )}

        {/* FOOTER */}
        <footer className="footer">
          <span>© 2026 MelodyAI Studio</span>
          <span>
            Made for music lovers <span className="footer-heart">♥</span>
          </span>
        </footer>
      </main>
    </div>
  );
}

export default App;
