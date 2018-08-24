import React from 'react';
import { Redirect } from 'react-router-dom';

const Form = (props) => {
  const {
    isAuthenticated, formType, handleUserFormSubmit, formData, handleFormChange,
  } = props;

  if (isAuthenticated) {
    return <Redirect to="/" />;
  }

  return (
    <div>
      <h1>{formType}</h1>
      <hr />
      <br />
      <form onSubmit={event => handleUserFormSubmit(event)}>
        {formType === 'Register' && (
        <div className="form-group">
          <input
            name="username"
            className="form-control input-lg"
            type="text"
            placeholder="Enter a username"
            required
            value={formData.username}
            onChange={handleFormChange}
          />
        </div>)
    }
        <div className="form-group">
          <input
            name="email"
            className="form-control input-lg"
            type="email"
            placeholder="Enter an email address"
            required
            value={formData.email}
            onChange={handleFormChange}
          />
        </div>
        <div className="form-group">
          <input
            name="password"
            className="form-control input-lg"
            type="password"
            placeholder="Enter a password"
            required
            value={formData.password}
            onChange={handleFormChange}
          />
        </div>
        <input
          type="submit"
          className="btn btn-primary btn-lg btn-block"
          value="Submit"
        />
      </form>
    </div>
  );
};

export default Form;
