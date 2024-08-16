// import React, { useState } from 'react';
// import './styles.css';
//
// function Login({ onLogin }) {
//     const [email, setEmail] = useState('');
//     const [password, setPassword] = useState('');
//
//     const handleSubmit = (event) => {
//         event.preventDefault();
//         // Ở đây bạn có thể thêm logic xác thực đăng nhập
//         if (email === 'admin@example.com' && password === 'password') {
//             onLogin();
//         } else {
//             alert('Invalid credentials');
//         }
//     };
//
//     return (
//         <div className="login-container">
//             <form onSubmit={handleSubmit}>
//                 <div className="svgContainer">
//                     <div>
//                         <svg className="mySVG" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" viewBox="0 0 200 200">
//                             <defs>
//                                 <circle id="armMaskPath" cx="100" cy="100" r="100"/>
//                             </defs>
//                             <clipPath id="armMask">
//                                 <use href="#armMaskPath" overflow="visible"/>
//                             </clipPath>
//                             <circle cx="100" cy="100" r="100" fill="#a9ddf3"/>
//                             <g className="body">
//                                 <path fill="#FFFFFF" d="M193.3,135.9c-5.8-8.4-15.5-13.9-26.5-13.9H151V72c0-27.6-22.4-50-50-50S51,44.4,51,72v50H32.1 c-10.6,0-20,5.1-25.8,13l0,78h187L193.3,135.9z"/>
//                                 <path fill="none" stroke="#3A5E77" strokeWidth="2.5" strokeLinecap="round" stroke-linejoinn="round" d="M193.3,135.9 c-5.8-8.4-15.5-13.9-26.5-13.9H151V72c0-27.6-22.4-50-50-50S51,44.4,51,72v50H32.1c-10.6,0-20,5.1-25.8,13"/>
//                                 <path fill="#DDF1FA" d="M100,156.4c-22.9,0-43,11.1-54.1,27.7c15.6,10,34.2,15.9,54.1,15.9s38.5-5.8,54.1-15.9 C143,167.5,122.9,156.4,100,156.4z"/>
//                             </g>
//                             <g className="earL">
//                                 <g className="outerEar" fill="#ddf1fa" stroke="#3a5e77" strokeWidth="2.5">
//                                     <path d="M38.8,105.3c2.7,0.4,5.2-1.2,5.9-3.9c0.6-2.7-0.9-5.3-3.4-5.9c-0.5-0.1-1-0.1-1.5,0L38.8,105.3z"/>
//                                     <path d="M43.4,100.4c0,0-0.5-0.4-1.5-0.1c-2.2,0.5-3.8,3.3-3.4,5.9c0.2,1,0.8,1.7,1.7,2.2C41.4,107.4,43.4,100.4,43.4,100.4z"/>
//                                 </g>
//                                 <g className="earHair" fill="#3a5e77">
//                                     <path d="M38.6,97.5c0,0-1.2,1.3-2.8,0.8s-2-2.1-2-2.1S36.4,94.5,38.6,97.5z"/>
//                                     <path d="M38.6,97.5c0,0,0.7-1.5-1-2.8s-3.4-0.8-3.4-0.8S34.8,95.4,38.6,97.5z"/>
//                                     <path d="M38.5,97.7c0,0,1.1-1.4,2.8-0.8c1.6,0.5,2,2.2,2,2.2S38.5,97.7,38.5,97.7z"/>
//                                     <path d="M38.5,97.7c0,0-0.6,1.6,1.1,2.8c1.6,1.1,3.4,0.6,3.4,0.6S41.6,96.3,38.5,97.7z"/>
//                                 </g>
//                             </g>
//                             <g className="earR">
//                                 <g className="outerEar" fill="#ddf1fa" stroke="#3a5e77" strokeWidth="2.5">
//                                     <path d="M161.2,105.3c-2.7,0.4-5.2-1.2-5.9-3.9c-0.6-2.7,0.9-5.3,3.4-5.9c0.5-0.1,1-0.1,1.5,0L161.2,105.3z"/>
//                                     <path d="M156.6,100.4c0,0,0.5-0.4,1.5-0.1c2.2,0.5,3.8,3.3,3.4,5.9c-0.2,1-0.8,1.7-1.7,2.2C158.6,107.4,156.6,100.4,156.6,100.4z"/>
//                                 </g>
//                                 <g className="earHair" fill="#3a5e77">
//                                     <path d="M161.4,97.5c0,0,1.2,1.3,2.8,0.8s2-2.1,2-2.1S163.6,94.5,161.4,97.5z"/>
//                                     <path d="M161.4,97.5c0,0-0.7-1.5,1-2.8c1.7-1.3,3.4-0.8,3.4-0.8S165.2,95.4,161.4,97.5z"/>
//                                     <path d="M161.5,97.7c0,0-1.1-1.4-2.8-0.8c-1.6,0.5-2,2.2-2,2.2S161.5,97.7,161.5,97.7z"/>
//                                     <path d="M161.5,97.7c0,0,0.6,1.6-1.1,2.8c-1.6,1.1-3.4,0.6-3.4,0.6S158.4,96.3,161.5,97.7z"/>
//                                 </g>
//                             </g>
//                         </svg>
//                     </div>
//                 </div>
//                 <div className="inputGroup inputGroup1">
//                     <input
//                         id="email"
//                         type="email"
//                         value={email}
//                         onChange={(e) => setEmail(e.target.value)}
//                         required
//                     />
//                     <label htmlFor="email">Email</label>
//                     <span className="helper helper1">Enter your email</span>
//                 </div>
//                 <div className="inputGroup">
//                     <input
//                         id="password"
//                         type="password"
//                         value={password}
//                         onChange={(e) => setPassword(e.target.value)}
//                         required
//                     />
//                     <label htmlFor="password" >Password</label>
//                 </div>
//                 <button type="submit">Login</button>
//             </form>
//         </div>
//     );
// }
//
// export default Login;



// import React, {useState} from 'react';
import { GoogleLogin } from '@react-oauth/google'; // Import GoogleLogin
import { jwtDecode } from 'jwt-decode'; // Import jwt-decode để giải mã thông tin người dùng từ token
import './styles.css';


function Login({ onLogin }) {

    //     const [email, setEmail] = useState('');
    // const [password, setPassword] = useState('');

    // const handleSubmit = (event) => {
    //     event.preventDefault();
    //     // Ở đây bạn có thể thêm logic xác thực đăng nhập
    //     if (email === 'admin@example.com' && password === 'password') {
    //         onLogin();
    //     } else {
    //         alert('Invalid credentials');
    //     }
    // };


    const handleGoogleSuccess = (response) => {
        const userObject = jwtDecode(response.credential);
        console.log(userObject); // In thông tin người dùng
        onLogin();
    };

    const handleGoogleFailure = (response) => {
        console.error('Login failed: ', response);
    };

    return (
        <div className="login-container">
            <form >
                <div className="svgContainer">
                    <div>
                     <svg className="mySVG" xmlns="http://www.w3.org/2000/svg"
                            xmlnsXlink="http://www.w3.org/1999/xlink" viewBox="0 0 200 200">
                     <defs>
                     <circle id="armMaskPath" cx="100" cy="100" r="100"/>
                     </defs>
                     <clipPath id="armMask">
                     <use href="#armMaskPath" overflow="visible"/>
                     </clipPath>
                     <circle cx="100" cy="100" r="100" fill="#a9ddf3"/>
                     <g className="body">
                     <path fill="#FFFFFF"
                             d="M193.3,135.9c-5.8-8.4-15.5-13.9-26.5-13.9H151V72c0-27.6-22.4-50-50-50S51,44.4,51,72v50H32.1 c-10.6,0-20,5.1-25.8,13l0,78h187L193.3,135.9z"/>
                     <path fill="none" stroke="#3A5E77" strokeWidth="2.5" strokeLinecap="round"
                             stroke-linejoinn="round"
                             d="M193.3,135.9 c-5.8-8.4-15.5-13.9-26.5-13.9H151V72c0-27.6-22.4-50-50-50S51,44.4,51,72v50H32.1c-10.6,0-20,5.1-25.8,13"/>
                     <path fill="#DDF1FA"
                             d="M100,156.4c-22.9,0-43,11.1-54.1,27.7c15.6,10,34.2,15.9,54.1,15.9s38.5-5.8,54.1-15.9 C143,167.5,122.9,156.4,100,156.4z"/>
                     </g>
                     <g className="earL">
                     <g className="outerEar" fill="#ddf1fa" stroke="#3a5e77" strokeWidth="2.5">
                     <path
                    d="M38.8,105.3c2.7,0.4,5.2-1.2,5.9-3.9c0.6-2.7-0.9-5.3-3.4-5.9c-0.5-0.1-1-0.1-1.5,0L38.8,105.3z"/>
                     <path
                    d="M43.4,100.4c0,0-0.5-0.4-1.5-0.1c-2.2,0.5-3.8,3.3-3.4,5.9c0.2,1,0.8,1.7,1.7,2.2C41.4,107.4,43.4,100.4,43.4,100.4z"/>
                     </g>
                     <g className="earHair" fill="#3a5e77">
                     <path d="M38.6,97.5c0,0-1.2,1.3-2.8,0.8s-2-2.1-2-2.1S36.4,94.5,38.6,97.5z"/>
                     <path d="M38.6,97.5c0,0,0.7-1.5-1-2.8s-3.4-0.8-3.4-0.8S34.8,95.4,38.6,97.5z"/>
                     <path d="M38.5,97.7c0,0,1.1-1.4,2.8-0.8c1.6,0.5,2,2.2,2,2.2S38.5,97.7,38.5,97.7z"/>
                     <path d="M38.5,97.7c0,0-0.6,1.6,1.1,2.8c1.6,1.1,3.4,0.6,3.4,0.6S41.6,96.3,38.5,97.7z"/>
                     </g>
                     </g>
                     <g className="earR">
                     <g className="outerEar" fill="#ddf1fa" stroke="#3a5e77" strokeWidth="2.5">
                     <path
                    d="M161.2,105.3c-2.7,0.4-5.2-1.2-5.9-3.9c-0.6-2.7,0.9-5.3,3.4-5.9c0.5-0.1,1-0.1,1.5,0L161.2,105.3z"/>
                     <path
                    d="M156.6,100.4c0,0,0.5-0.4,1.5-0.1c2.2,0.5,3.8,3.3,3.4,5.9c-0.2,1-0.8,1.7-1.7,2.2C158.6,107.4,156.6,100.4,156.6,100.4z"/>
                     </g>
                     <g className="earHair" fill="#3a5e77">
                     <path d="M161.4,97.5c0,0,1.2,1.3,2.8,0.8s2-2.1,2-2.1S163.6,94.5,161.4,97.5z"/>
                     <path d="M161.4,97.5c0,0-0.7-1.5,1-2.8c1.7-1.3,3.4-0.8,3.4-0.8S165.2,95.4,161.4,97.5z"/>
                     <path d="M161.5,97.7c0,0-1.1-1.4-2.8-0.8c-1.6,0.5-2,2.2-2,2.2S161.5,97.7,161.5,97.7z"/>
                     <path d="M161.5,97.7c0,0,0.6,1.6-1.1,2.8c-1.6,1.1-3.4,0.6-3.4,0.6S158.4,96.3,161.5,97.7z"/>
                     </g>
                     </g>
                     </svg>
                     </div>

                </div>


            <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onFailure={handleGoogleFailure}
                cookiePolicy={'single_host_origin'}
            />
            </form>
        </div>
);
}

export default Login;
