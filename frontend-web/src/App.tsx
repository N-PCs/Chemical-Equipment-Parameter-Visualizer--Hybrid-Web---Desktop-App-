import { Navbar } from './components/layout/Navbar';
import { Container } from './components/layout/Container';
import { Dashboard } from './components/dashboard/Dashboard';
import './App.css';

function App() {
  return (
    <div className="app">
      <Navbar />
      <Container>
        <Dashboard />
      </Container>
    </div>
  );
}

export default App;
