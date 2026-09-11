import "./landingpage.css";

function LandingPage({ onStart }) {
  return (
    <div className="landing-page">

      <div className="landing-glow glow-one"></div>
      <div className="landing-glow glow-two"></div>

      <main className="landing-content">

        <div className="logo">
          Dr Brutally<span>Honest</span>
        </div>

        <div className="badge">
          Best Therapist Ever
        </div>

        <h1>
          Your problems
          <br />
          deserve better.
          <br />
          <span>Unfortunately, you got me.</span>
        </h1>

        <p className="description">
          Dr Brutally honest is an AI that listens to your problems,
          gives you brutally honest advice <br />   He is not like those lame therapists. <br />
          He is built different

        </p>

        <p className="warning">
          
        </p>

        <button className="start-button" onClick={onStart}>
          START SESSION
          <span>→</span>
        </button>

        <p className="disclaimer">
            *Only for entertainment purposes <br/>
          Not a real therapist. Please don't sue us.
        </p>

      </main>

      <div className="floating-text text-one">
        overthinking detected
      </div>

      <div className="floating-text text-two">
        probably your fault
      </div>

      <div className="floating-text text-three">
        💀
      </div>

    </div>
  );
}

export default LandingPage;