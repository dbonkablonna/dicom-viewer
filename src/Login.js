import React, { useState } from 'react';
import './Login.css';
import axios from "axios";

function Login({ onLogin }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        // Giả sử bạn có API đăng nhập để lấy token
        try {
            const response = await axios.post('http://localhost:5000/login', { email, password });
            const token = response.data.token;
            onLogin(token);
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="svgContainer">
                <div>
                    <svg className="mySVG" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" viewBox="0 0 200 200">
                        {/* SVG nội dung ở đây */}
                    </svg>
                </div>
            </div>
            <div className="inputGroup inputGroup1">
                <input
                    id="email"
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <label htmlFor="email">Email</label>
                <span className="helper helper1">Enter your email</span>
            </div>
            <div className="inputGroup">
                <input
                    id="password"
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <label htmlFor="password">Password</label>
            </div>
            <button type="submit">Login</button>
        </form>
    );
}

export default Login;
